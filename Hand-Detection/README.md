# Finger Counting Project

A real-time finger counting application using computer vision and OpenCV. The system detects hand gestures through webcam input and counts the number of extended fingers (0-5).

## Features

- Real-time finger detection using webcam
- Skin tone segmentation with YCrCb/HSV color spaces
- Convex hull and convexity defects analysis for finger counting
- Live FPS display and skin mask visualization
- Screenshot capture functionality

## Installation

1. Clone or download the project files
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main demo:
```bash
python main.py
```

### Controls
- **'q'**: Quit the application
- **'s'**: Save screenshot with current frame

## Demo Tips

### Optimal Conditions
- **Lighting**: Use good, even lighting. Avoid harsh shadows or very dim conditions
- **Background**: Simple, non-skin-colored background works best (white wall, dark surface)
- **Distance**: Keep hand 1-2 feet from camera for best detection
- **Position**: Center your hand in the camera view

### Hand Positioning
- Show palm facing the camera
- Keep fingers clearly separated
- Avoid covering fingers with each other
- Move slowly for better tracking

## Example Gestures to Test

| Fingers | Gesture | Description |
|---------|---------|-------------|
| 0 | Closed fist | Make a tight fist |
| 1 | Index finger | Point with index finger |
| 2 | Peace sign | Index and middle finger extended |
| 3 | Three fingers | Index, middle, and ring finger |
| 4 | Four fingers | All fingers except thumb |
| 5 | Open hand | All five fingers extended |

## Project Structure

```
Hand Detection/
├── main.py           # Main demo application
├── utils.py          # Core processing functions
├── requirements.txt  # Package dependencies
└── README.md        # Project documentation
```

## Functions Overview

- `preprocess_frame()`: Converts frame to skin mask using color filtering
- `find_largest_contour()`: Finds the largest hand contour in the mask
- `count_fingers()`: Analyzes contour to count extended fingers

## Troubleshooting

- **No detection**: Check lighting and background conditions
- **Incorrect count**: Ensure fingers are clearly separated and visible
- **Poor performance**: Reduce frame size or check system resources
- **Camera issues**: Verify webcam is connected and not used by other applications

## Requirements

- Python 3.7+
- OpenCV 4.x
- NumPy
- Webcam/camera device
