# motion_detector.py
"""
Motion detection functions for the sports video analysis project.
"""

import numpy as np
from skimage import color, filters, morphology, measure
from skimage.morphology import binary_dilation, disk


def detect_motion(frames, frame_idx, threshold=0.1, min_area=500):
    """
    Detect motion in the current frame by comparing with previous frame.

    Args:
        frames: List of video frames
        frame_idx: Index of the current frame
        threshold: Threshold for frame difference detection (0-1 range for skimage)
        min_area: Minimum region area to consider

    Returns:
        List of bounding boxes for detected motion regions
    """
    if frame_idx < 1 or frame_idx >= len(frames):
        return []
    
    current_frame = frames[frame_idx]
    prev_frame = frames[frame_idx - 1]

    # Convert frames to grayscale
    current_gray = color.rgb2gray(current_frame)
    prev_gray = color.rgb2gray(prev_frame)
    
    # Apply Gaussian blur to reduce noise
    current_blurred = filters.gaussian(current_gray, sigma=1.0)
    prev_blurred = filters.gaussian(prev_gray, sigma=1.0)
    
    # Calculate absolute difference between frames
    frame_diff = np.abs(current_blurred - prev_blurred)
    
    # Apply threshold to highlight differences
    binary_diff = frame_diff > threshold
    
    # Apply morphological operations to fill holes and connect nearby regions
    selem = disk(3)
    dilated = binary_dilation(binary_diff, selem)
    
    cleaned = morphology.remove_small_objects(dilated, min_size=min_area//10)
    

    labeled_regions = measure.label(cleaned)
    regions = measure.regionprops(labeled_regions)
    
    # Extract bounding boxes from regions that meet area criteria
    motion_boxes = []
    for region in regions:
        if region.area >= min_area:
            min_row, min_col, max_row, max_col = region.bbox
            
            # Convert to (x, y, width, height) format
            x = min_col
            y = min_row
            width = max_col - min_col
            height = max_row - min_row
            
            motion_boxes.append((x, y, width, height))
    
    return motion_boxes