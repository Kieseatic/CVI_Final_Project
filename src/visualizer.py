# visualizer.py
"""
Visualization functions for displaying motion detection and viewport tracking results.
"""

import os
import numpy as np
import imageio
from skimage import draw
from skimage.util import img_as_ubyte


def draw_rectangle(image, x, y, width, height, color, thickness=2):
    """
    Draw a rectangle on an image using skimage.
    
    Args:
        image: Input image array
        x, y: Top-left corner coordinates
        width, height: Rectangle dimensions
        color: RGB color tuple (r, g, b)
        thickness: Line thickness
    """

    img_copy = image.copy()
    
  
    h, w = img_copy.shape[:2]
    

    x1, y1 = max(0, x), max(0, y)
    x2, y2 = min(w-1, x + width), min(h-1, y + height)
    
   
    for t in range(thickness):
    
        x1_t, y1_t = max(0, x1 - t), max(0, y1 - t)
        x2_t, y2_t = min(w-1, x2 + t), min(h-1, y2 + t)
        
       
        if y1_t < h and y2_t < h:
            rr_top, cc_top = draw.line(y1_t, x1_t, y1_t, x2_t)
            rr_bottom, cc_bottom = draw.line(y2_t, x1_t, y2_t, x2_t)
            
        
            valid_top = (rr_top < h) & (cc_top < w) & (rr_top >= 0) & (cc_top >= 0)
            valid_bottom = (rr_bottom < h) & (cc_bottom < w) & (rr_bottom >= 0) & (cc_bottom >= 0)
            
            if len(color) == 3:  
                img_copy[rr_top[valid_top], cc_top[valid_top]] = color
                img_copy[rr_bottom[valid_bottom], cc_bottom[valid_bottom]] = color
        
      
        if x1_t < w and x2_t < w:
            rr_left, cc_left = draw.line(y1_t, x1_t, y2_t, x1_t)
            rr_right, cc_right = draw.line(y1_t, x2_t, y2_t, x2_t)
            
        
            valid_left = (rr_left < h) & (cc_left < w) & (rr_left >= 0) & (cc_left >= 0)
            valid_right = (rr_right < h) & (cc_right < w) & (rr_right >= 0) & (cc_right >= 0)
            
            if len(color) == 3:  
                img_copy[rr_left[valid_left], cc_left[valid_left]] = color
                img_copy[rr_right[valid_right], cc_right[valid_right]] = color
    
    return img_copy


def add_text_overlay(image, text, position, font_size=20):
    """
    Add text overlay to image (simplified version without OpenCV).
    
    Args:
        image: Input image array
        text: Text to add
        position: (x, y) position for text
        font_size: Font size (not used in this simple implementation)
    """
  
    img_copy = image.copy()
    x, y = position
    
    
    text_width = len(text) * 10 
    text_height = 20
    
    if y >= 0 and x >= 0 and y + text_height < img_copy.shape[0] and x + text_width < img_copy.shape[1]:
      
        img_copy[y:y+text_height, x:x+text_width] = [0, 0, 0] 
    
    return img_copy


def visualize_results(frames, motion_results, viewport_positions, viewport_size, output_dir):
    """
    Create visualization of motion detection and viewport tracking results.

    Args:
        frames: List of video frames
        motion_results: List of motion detection results for each frame
        viewport_positions: List of viewport center positions for each frame
        viewport_size: Tuple (width, height) of the viewport
        output_dir: Directory to save visualization results
    """
   
    frames_dir = os.path.join(output_dir, "frames")
    viewport_dir = os.path.join(output_dir, "viewport")
    os.makedirs(frames_dir, exist_ok=True)
    os.makedirs(viewport_dir, exist_ok=True)

    height, width = frames[0].shape[:2]
    vp_width, vp_height = viewport_size

    
    visualization_frames = []
    viewport_frames = []

 
    for i, frame in enumerate(frames):
   
        vis_frame = frame.copy()
        
      
        motion_boxes = motion_results[i] if i < len(motion_results) else []
        vp_center = viewport_positions[i] if i < len(viewport_positions) else (width//2, height//2)
        
       
        for box in motion_boxes:
            x, y, w, h = box
            vis_frame = draw_rectangle(vis_frame, x, y, w, h, (0, 255, 0), thickness=3)
        
     
        vp_x, vp_y = vp_center
        vp_left = vp_x - vp_width // 2
        vp_top = vp_y - vp_height // 2
        vis_frame = draw_rectangle(vis_frame, vp_left, vp_top, vp_width, vp_height, (255, 0, 0), thickness=3)
        
     
        vis_frame = add_text_overlay(vis_frame, f"Frame {i+1}", (10, 30))
        
   
        vp_left = max(0, vp_left)
        vp_top = max(0, vp_top)
        vp_right = min(width, vp_left + vp_width)
        vp_bottom = min(height, vp_top + vp_height)
        
        viewport_frame = frame[vp_top:vp_bottom, vp_left:vp_right]
        
       
        if viewport_frame.shape[0] != vp_height or viewport_frame.shape[1] != vp_width:
            padded_viewport = np.zeros((vp_height, vp_width, 3), dtype=np.uint8)
            h_actual, w_actual = viewport_frame.shape[:2]
            padded_viewport[:h_actual, :w_actual] = viewport_frame
            viewport_frame = padded_viewport
        
      
        frame_filename = os.path.join(frames_dir, f"frame_{i+1:04d}.png")
        viewport_filename = os.path.join(viewport_dir, f"viewport_{i+1:04d}.png")
        
        imageio.imwrite(frame_filename, img_as_ubyte(vis_frame))
        imageio.imwrite(viewport_filename, img_as_ubyte(viewport_frame))
        
       
        visualization_frames.append(img_as_ubyte(vis_frame))
        viewport_frames.append(img_as_ubyte(viewport_frame))
    
  
    video_path = os.path.join(output_dir, "motion_detection.mp4")
    viewport_video_path = os.path.join(output_dir, "viewport_tracking.mp4")
    

    with imageio.get_writer(video_path, fps=5) as writer:
        for frame in visualization_frames:
            writer.append_data(frame)
    
   
    with imageio.get_writer(viewport_video_path, fps=5) as writer:
        for frame in viewport_frames:
            writer.append_data(frame)

    print(f"Visualization saved to {video_path}")
    print(f"Viewport video saved to {viewport_video_path}")
    print(f"Individual frames saved to {frames_dir} and {viewport_dir}")