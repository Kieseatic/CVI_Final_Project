# Sports Motion Detection & Viewport Tracking

A Python-based motion detection and viewport tracking system that simulates a "virtual camera" following the main action in sports video clips.

## Project Overview

This project implements a computer vision system that:
- Extracts frames from sports videos at a target frame rate (~5 fps)
- Detects motion between consecutive frames using frame differencing
- Tracks the primary region of activity with intelligent viewport positioning
- Applies smoothing algorithms to create smooth camera movement
- Generates visualization videos showing both motion detection and viewport tracking

## Features

- **Frame Processing**: Efficient video frame extraction and resizing using imageio
- **Motion Detection**: Frame differencing with Gaussian blur, thresholding, and morphological operations
- **Intelligent Tracking**: Weighted average region of interest calculation based on motion area
- **Smooth Movement**: Exponential smoothing to prevent jerky camera movements
- **Dual Output**: Original video with overlays + cropped viewport video
- **Flexible Parameters**: Configurable viewport size, smoothing factor, and detection thresholds

## Technology Stack

- **Python 3.8+**
- **scikit-image**: Image processing and computer vision operations
- **imageio**: Video I/O and format handling
- **NumPy**: Numerical computations and array operations
- **SciPy**: Scientific computing functions

## Installation

1. Install required packages:
```bash
pip install -r requirement.txt
```

## Usage

### Basic Usage
```bash
python src/main.py --video data/sample_video_clip.mp4 --output output
```

### Advanced Options
```bash
python src/main.py --video data/your_video.mp4 \
                   --output results \
                   --fps 5 \
                   --viewport_size 720x480
```

### Command Line Arguments

- `--video`: Path to input video file (required)
- `--output`: Output directory for results (default: "output")
- `--fps`: Target frames per second for processing (default: 5)
- `--viewport_size`: Viewport dimensions in WIDTHxHEIGHT format (default: "720x480")

## Output Structure

The system generates the following outputs:
```
output/
├── motion_detection.mp4      # Video with motion boxes and viewport overlay
├── viewport_tracking.mp4     # Cropped viewport content
├── frames/                   # Individual visualization frames
│   ├── frame_0001.png
│   ├── frame_0002.png
│   └── ...
└── viewport/                 # Individual viewport frames
    ├── viewport_0001.png
    ├── viewport_0002.png
    └── ...
```

## Algorithm Details

### Motion Detection
1. **Preprocessing**: Convert frames to grayscale and apply Gaussian blur
2. **Frame Differencing**: Calculate absolute difference between consecutive frames
3. **Thresholding**: Apply binary threshold to highlight significant changes
4. **Morphological Operations**: Use dilation to connect nearby motion regions
5. **Region Analysis**: Find connected components and filter by minimum area

### Viewport Tracking
1. **Region of Interest**: Calculate weighted average of motion regions by area
2. **Smoothing**: Apply exponential moving average for smooth transitions
3. **Boundary Constraints**: Ensure viewport remains within frame boundaries
4. **Fallback Handling**: Default to frame center when no motion detected

### Visualization
- **Green Rectangles**: Motion detection bounding boxes
- **Blue Rectangle**: Current viewport position
- **Frame Numbers**: Overlay for tracking progress

## Configuration

Key parameters can be adjusted in the source code:

**Motion Detection** (`motion_detector.py`):
- `threshold`: Motion sensitivity (default: 0.1)
- `min_area`: Minimum motion region size (default: 500)

**Viewport Tracking** (`viewport_tracker.py`):
- `smoothing_factor`: Movement smoothing (default: 0.3, lower = smoother)

## Project Structure

```
├── src/
│   ├── main.py               # Main pipeline orchestration
│   ├── frame_processor.py    # Video frame extraction and processing
│   ├── motion_detector.py    # Motion detection algorithms
│   ├── viewport_tracker.py   # Viewport tracking and smoothing
│   └── visualizer.py         # Output generation and visualization
├── data/
│   └── sample_video_clip.mp4 # Sample input video
├── requirement.txt           # Python dependencies
└── README.md                 # This file
```

## Implementation Notes

This implementation uses **scikit-image** instead of OpenCV to work within the project's package constraints. Key design decisions:

- **Frame differencing** over optical flow for simplicity and robustness
- **Area-weighted averaging** for handling multiple motion regions
- **Exponential smoothing** for natural camera movement
- **Boundary-aware positioning** to prevent viewport clipping
- **Dual visualization** for comprehensive analysis

## Performance Considerations

- Processing speed depends on video resolution and frame rate
- Memory usage scales with video length and frame dimensions
- Recommended for videos up to 30 seconds at 1280x720 resolution
- Motion detection parameters may need tuning for different sports/scenes

## Course Information

**CVI620 Final Project - Summer 2025**  
**Instructor**: Ellie Azizi  
**Project Type**: Sports Motion Detection & Viewport Tracking
