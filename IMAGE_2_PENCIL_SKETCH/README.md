# Image to Pencil Sketch Converter

A professional GUI application that transforms digital images into artistic pencil sketches using advanced computer vision techniques with OpenCV and Python.

## Overview

This application provides an intuitive graphical interface for converting photographs and digital images into realistic pencil sketch representations. The conversion process utilizes grayscale transformation, Gaussian blur operations, and mathematical division techniques enhanced with gamma correction for optimal visual results.

## Features

- **Intuitive GUI Interface**: Clean Tkinter-based interface with side-by-side image comparison
- **Real-time Processing**: Background threading ensures responsive user experience
- **Customizable Parameters**: Adjustable blur intensity and scale factors
- **Gamma Correction**: Enhanced darkening control for more realistic sketch appearance
- **Multi-format Support**: Compatible with JPG, PNG, BMP, TIFF image formats
- **Keyboard Shortcuts**: Quick access via Ctrl+O (Open), Ctrl+S (Save), Enter (Process)
- **Error Handling**: Comprehensive error management with user-friendly messages

## Technical Implementation

### Core Algorithm
1. **Grayscale Conversion**: RGB to grayscale transformation using OpenCV
2. **Gaussian Blur**: Applies configurable blur kernel for smoothing
3. **Division Operation**: Creates sketch effect through `cv2.divide(gray, blurred, scale)`
4. **Gamma Correction**: Applies `np.power(sketch/255.0, gamma)` for enhanced darkness control

### Key Functions

#### `convert_to_sketch_cv2()`
- **Purpose**: Main image processing function
- **Parameters**: 
  - `image_path`: Source image file path
  - `blur_ksize`: Gaussian blur kernel size (must be odd, ≥1)
  - `scale`: Division operation scaling factor
  - `gamma`: Gamma correction value for darkness adjustment
- **Returns**: Processed uint8 numpy array (grayscale sketch)

#### `cv2_to_pil_gray()` & `cv2_to_pil_bgr()`
- **Purpose**: Format conversion utilities between OpenCV and PIL
- **Usage**: Enables seamless integration with Tkinter display components

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation Steps

1. **Clone or Download Project**
   ```bash
   git clone <repository-url>
   cd IMAGE_2_PENCIL_SKETCH
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage Guide

### Running the Application
```bash
python main.py
```

### Operating Instructions
1. **Load Image**: Click "Open Image" or use Ctrl+O to select source image
2. **Adjust Parameters**: 
   - **Blur**: Set kernel size (recommended: 21)
   - **Scale**: Set division scale (recommended: 256)
3. **Generate Sketch**: Click "Create Sketch" or press Enter
4. **Save Result**: Click "Save Sketch" or use Ctrl+S to export

### Recommended Parameters
- **Blur Kernel Size**: 21 (produces optimal smoothing)
- **Scale Factor**: 256 (provides balanced contrast)
- **Gamma Value**: 0.8 (default darkening for realistic appearance)

## Dependencies

```
opencv-python>=4.5.0    # Computer vision operations
numpy>=1.19.0           # Numerical computations
pillow>=8.0.0          # Image format handling
```

## Project Structure

```
IMAGE_2_PENCIL_SKETCH/
├── main.py              # GUI application entry point
├── utils.py             # Core image processing utilities
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
└── venv/               # Virtual environment (excluded from git)
```

## Error Handling

The application includes comprehensive error management:
- **File Validation**: Verifies image file accessibility
- **Parameter Validation**: Ensures blur kernel requirements
- **Processing Errors**: Graceful handling with user notifications
- **Memory Management**: Efficient resource utilization

## Performance Considerations

- **Background Processing**: Non-blocking UI during image processing
- **Memory Optimization**: Efficient numpy array handling
- **Image Scaling**: Automatic resize for display optimization
- **Threading**: Daemon threads prevent application hanging

## Future Enhancements

- Batch processing capabilities
- Additional artistic filters
- Color sketch options
- Export format selection
- Processing history

## Technical Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, Linux Ubuntu 18.04+
- **Memory**: Minimum 4GB RAM recommended
- **Storage**: 100MB available space
- **Display**: 1024x768 minimum resolution

## License

This project is available for educational and personal use. Commercial usage requires appropriate licensing of OpenCV and other dependencies.

## Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 standards
- Functions include comprehensive docstrings
- Error handling is implemented
- Testing is performed across multiple image formats

