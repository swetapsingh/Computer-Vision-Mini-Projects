import cv2
import time
import numpy as np
from utils import preprocess_frame, find_largest_contour, count_fingers


def main():
    """
    Main function for realtime finger counting demo using webcam.
    """
    print("Starting finger counting demo...")
    print("Controls: 'q' to quit, 's' to save screenshot")
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    print("Webcam opened successfully")
    
    # Variables for FPS calculation
    fps_counter = 0
    fps_start_time = time.time()
    current_fps = 0
    
    # Screenshot counter for unique filenames
    screenshot_count = 0
    
    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read frame from webcam")
            break
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Resize frame for better performance
        frame = cv2.resize(frame, (640, 480))
        
        # Get skin mask using utils function
        mask = preprocess_frame(frame, method='ycrcb')
        
        # Find largest contour (hand)
        contour = find_largest_contour(mask)
        
        finger_count = 0
        
        # Count fingers if hand contour is found
        if contour is not None:
            finger_count, frame = count_fingers(contour, frame)
        
        # Display finger count text
        cv2.putText(frame, f'Fingers: {finger_count}', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Calculate and display FPS
        fps_counter += 1
        if fps_counter % 10 == 0:  # Update FPS every 10 frames
            fps_end_time = time.time()
            current_fps = 10 / (fps_end_time - fps_start_time)
            fps_start_time = fps_end_time
        
        cv2.putText(frame, f'FPS: {current_fps:.1f}', (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
        # Create small mask display for assistance
        mask_small = cv2.resize(mask, (160, 120))  # Quarter size
        mask_colored = cv2.cvtColor(mask_small, cv2.COLOR_GRAY2BGR)
        
        # Position mask display at top-right corner
        frame[10:130, 470:630] = mask_colored
        
        # Add border around mask display
        cv2.rectangle(frame, (470, 10), (630, 130), (255, 255, 255), 2)
        cv2.putText(frame, 'Skin Mask', (475, 145), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Add instructions text
        cv2.putText(frame, "Press 'q' to quit, 's' to save", (10, 460), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        # Display the frame
        cv2.imshow('Finger Counting Demo', frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("Quit key pressed. Exiting...")
            break
        elif key == ord('s'):
            # Save screenshot
            screenshot_count += 1
            filename = f'screenshot_{screenshot_count:03d}.jpg'
            cv2.imwrite(filename, frame)
            print(f"Screenshot saved as {filename}")
            
            # Show brief save confirmation on frame
            save_frame = frame.copy()
            cv2.putText(save_frame, 'SAVED!', (250, 240), 
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            cv2.imshow('Finger Counting Demo', save_frame)
            cv2.waitKey(500)  # Show for 500ms
    
    # Cleanup
    print("Releasing camera and closing windows...")
    cap.release()
    cv2.destroyAllWindows()
    print("Demo ended successfully")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure cleanup even if error occurs
        cv2.destroyAllWindows()
