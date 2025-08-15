# frame_processor.py
"""
Frame processing functions for the motion detection project.
"""

import imageio
import numpy as np
from skimage import transform


def process_video(video_path, target_fps=5, resize_dim=(1280, 720)):
    """
    Extract frames from a video at a specified frame rate.

    Args:
        video_path: Path to the video file
        target_fps: Target frames per second to extract
        resize_dim: Dimensions to resize frames to (width, height)

    Returns:
        List of extracted frames
    """
    frames = []
    
    try:
        reader = imageio.get_reader(video_path)
        video_fps = reader.get_meta_data()['fps']
        
        # Calculate frame interval
        frame_interval = max(1, int(video_fps / target_fps))
        
        print(f"Video FPS: {video_fps}, extracting every {frame_interval} frames")
        
        # Extract frames
        for i, frame in enumerate(reader):
            if i % frame_interval == 0:
                resized_frame = transform.resize(
                    frame, 
                    (resize_dim[1], resize_dim[0]),  
                    anti_aliasing=True,
                    preserve_range=True
                ).astype(np.uint8)
                
                frames.append(resized_frame)
        
        reader.close()
        
    except Exception as e:
        print(f"Error processing video {video_path}: {e}")
        return []
    
    return frames

