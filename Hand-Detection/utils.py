import cv2
import numpy as np
from typing import Optional, Tuple


def preprocess_frame(frame: np.ndarray, method: str = 'ycrcb') -> np.ndarray:
    """
    Convert BGR frame to a binary skin mask using color space filtering.
    
    Args:
        frame: Input BGR image as numpy array
        method: Color space method ('ycrcb' or 'hsv') for skin detection
        
    Returns:
        Binary mask (uint8) where white pixels represent detected skin
        
    Raises:
        ValueError: If method is not 'ycrcb' or 'hsv'
    """
    if method not in ['ycrcb', 'hsv']:
        raise ValueError("Method must be 'ycrcb' or 'hsv'")
    
    # Convert color space and apply skin detection
    if method == 'ycrcb':
        # YCrCb color space is effective for skin detection
        converted = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
        # Skin tone ranges in YCrCb
        lower_skin = np.array([0, 133, 77], dtype=np.uint8)
        upper_skin = np.array([255, 173, 127], dtype=np.uint8)
    else:  # hsv method
        # HSV color space alternative
        converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Skin tone ranges in HSV
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    # Create binary mask based on color range
    mask = cv2.inRange(converted, lower_skin, upper_skin)
    
    # Apply Gaussian blur to smooth the mask
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    
    # Morphological operations to clean up noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    
    # Opening: removes small noise
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # Closing: fills small holes
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    return mask


def find_largest_contour(mask: np.ndarray) -> Optional[np.ndarray]:
    """
    Find and return the largest contour by area from a binary mask.
    
    Args:
        mask: Binary image (numpy array) where contours will be detected
        
    Returns:
        Largest contour as numpy array, or None if no contours found
    """
    # Find all contours in the binary mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None
    
    # Find contour with maximum area
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Return None if the largest contour is too small (likely noise)
    if cv2.contourArea(largest_contour) < 1000:
        return None
        
    return largest_contour


def count_fingers(contour: np.ndarray, drawing: Optional[np.ndarray] = None) -> Tuple[int, np.ndarray]:
    """
    Count fingers using convex hull and convexity defects analysis.
    
    Args:
        contour: Hand contour as numpy array
        drawing: Optional image to draw results on (will be copied if provided)
        
    Returns:
        Tuple of (finger_count, drawing_image)
        - finger_count: Number of detected fingers (0-5)
        - drawing_image: Image with visual annotations (copy of input or black image)
    """
    # Create drawing canvas if not provided
    if drawing is not None:
        drawing = drawing.copy()
    else:
        # Create black image for visualization
        drawing = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Compute convex hull
    hull_indices = cv2.convexHull(contour, returnPoints=False)
    hull_points = cv2.convexHull(contour, returnPoints=True)
    
    # Draw contour and hull for visualization
    cv2.drawContours(drawing, [contour], -1, (0, 255, 0), 2)  # Green contour
    cv2.drawContours(drawing, [hull_points], -1, (0, 0, 255), 2)  # Red hull
    
    # Need at least 4 points to compute convexity defects
    if len(hull_indices) < 4:
        return 0, drawing
    
    # Compute convexity defects
    defects = cv2.convexityDefects(contour, hull_indices)
    
    if defects is None:
        return 0, drawing
    
    finger_count = 0
    
    # Analyze each defect to identify finger tips
    for i in range(defects.shape[0]):
        start_idx, end_idx, far_idx, depth = defects[i, 0]
        
        # Get the actual points
        start_point = tuple(contour[start_idx][0])
        end_point = tuple(contour[end_idx][0])
        far_point = tuple(contour[far_idx][0])
        
        # Calculate distances for angle computation
        a = np.linalg.norm(np.array(start_point) - np.array(end_point))
        b = np.linalg.norm(np.array(start_point) - np.array(far_point))
        c = np.linalg.norm(np.array(end_point) - np.array(far_point))
        
        # Calculate angle using law of cosines
        if b != 0 and c != 0:
            angle = np.arccos((b**2 + c**2 - a**2) / (2 * b * c))
            angle_deg = np.degrees(angle)
            
            # Filter defects: depth > 20 pixels and angle < 90 degrees
            # These criteria help identify valleys between fingers
            if depth > 20 and angle_deg < 90:
                finger_count += 1
                
                # Draw defect point (valley between fingers)
                cv2.circle(drawing, far_point, 5, (255, 0, 0), -1)  # Blue dot
                
                # Draw finger tip circles
                cv2.circle(drawing, start_point, 8, (255, 255, 0), -1)  # Cyan circle
    
    # Finger count is typically defects + 1 (but cap at 5)
    finger_count = min(finger_count + 1, 5)
    
    # Handle edge case: if no valid defects found, assume 1 finger
    if finger_count == 1 and len(defects) == 0:
        finger_count = 1
    
    return finger_count, drawing
