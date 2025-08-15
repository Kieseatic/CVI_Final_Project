# viewport_tracker.py
"""
Viewport tracking functions for creating a smooth "virtual camera".
"""

import numpy as np


def calculate_region_of_interest(motion_boxes, frame_shape):
    """
    Calculate the primary region of interest based on motion boxes.

    Args:
        motion_boxes: List of motion detection bounding boxes
        frame_shape: Shape of the video frame (height, width)

    Returns:
        Tuple (x, y, w, h) representing the region of interest center point and dimensions
    """
    if not motion_boxes:
        
        height, width = frame_shape[:2]
        return (width // 2, height // 2, 0, 0)

   
    total_area = 0
    weighted_x = 0
    weighted_y = 0
    max_area = 0
    largest_box = None
    
    for box in motion_boxes:
        x, y, w, h = box
        area = w * h
        
       
        center_x = x + w // 2
        center_y = y + h // 2
        
      
        weighted_x += center_x * area
        weighted_y += center_y * area
        total_area += area
        
     
        if area > max_area:
            max_area = area
            largest_box = box
    
    if total_area > 0:
   
        center_x = int(weighted_x / total_area)
        center_y = int(weighted_y / total_area)
        
       
        min_x = min(box[0] for box in motion_boxes)
        min_y = min(box[1] for box in motion_boxes)
        max_x = max(box[0] + box[2] for box in motion_boxes)
        max_y = max(box[1] + box[3] for box in motion_boxes)
        
        combined_width = max_x - min_x
        combined_height = max_y - min_y
        
        return (center_x, center_y, combined_width, combined_height)
    else:
      
        if largest_box:
            x, y, w, h = largest_box
            return (x + w // 2, y + h // 2, w, h)
        else:
       
            height, width = frame_shape[:2]
            return (width // 2, height // 2, 0, 0)


def track_viewport(frames, motion_results, viewport_size, smoothing_factor=0.3):
    """
    Track viewport position across frames with smoothing.

    Args:
        frames: List of video frames
        motion_results: List of motion detection results for each frame
        viewport_size: Tuple (width, height) of the viewport
        smoothing_factor: Factor for smoothing viewport movement (0-1)
                          Lower values create smoother movement

    Returns:
        List of viewport positions for each frame as (x, y) center coordinates
    """
    viewport_positions = []
    
    if not frames:
        return []
    
 
    frame_height, frame_width = frames[0].shape[:2]
    viewport_width, viewport_height = viewport_size
    

    prev_x = frame_width // 2
    prev_y = frame_height // 2
    
    for i, motion_boxes in enumerate(motion_results):
      
        roi_x, roi_y, roi_w, roi_h = calculate_region_of_interest(
            motion_boxes, frames[i].shape
        )
        
      
        target_x = roi_x
        target_y = roi_y
        
   
        smooth_x = int(prev_x * (1 - smoothing_factor) + target_x * smoothing_factor)
        smooth_y = int(prev_y * (1 - smoothing_factor) + target_y * smoothing_factor)
        
    
        half_vp_width = viewport_width // 2
        half_vp_height = viewport_height // 2
        
      
        min_x = half_vp_width
        max_x = frame_width - half_vp_width
        constrained_x = max(min_x, min(max_x, smooth_x))
        
     
        min_y = half_vp_height
        max_y = frame_height - half_vp_height
        constrained_y = max(min_y, min(max_y, smooth_y))
        
    
        viewport_positions.append((constrained_x, constrained_y))
        
      
        prev_x = constrained_x
        prev_y = constrained_y
    
    return viewport_positions
