# Sports Motion Detection & Viewport Tracking

This project processes an input video to:

1. **Extract frames**  
2. **Detect motion**  
3. **Track a moving viewport**  
4. **Render result videos**

The processed results (motion detection and viewport tracking videos) are saved to the specified output folder.

---

## Requirements

- Python 3.10+
- FFmpeg available via [`imageio-ffmpeg`]

> If you face issues installing libraries, try creating a Python virtual environment first (e.g., `python -m venv .venv` then activate it).

---

## Installation

```bash
pip install -r requirement.txt
pip install imageio-ffmpeg
```

---

## How to Run

```bash
python src/main.py   --video "./data/sample_video_clip.mp4"   --output "./output2"   --fps 5   --viewport_size 720x480
```

### Command Line Arguments

| Argument        | Description                                   | Default |
|-----------------|-----------------------------------------------|---------|
| `--video`       | Path to input video file **(required)**        | —       |
| `--output`      | Output directory to save results               | `output`|
| `--fps`         | Frames per second to process                   | `5`     |
| `--viewport_size` | Viewport width × height (format: `WxH`)     | `720x480` |

**Example:**

```bash
python src/main.py --video ./data/sample_video_clip.mp4 --output ./output2 --fps 8 --viewport_size 800x450
```

---

## Project Structure

```
CVI_Final_Project/
├── data/
│   └── sample_video_clip.mp4
├── output/                 
├── src/
│   ├── frame_processor.py
│   ├── motion_detector.py
│   ├── viewport_tracker.py
│   ├── visualizer.py
│   └── main.py
├── requirement.txt
└── README.md
```

---

## Expected Results

The output directory (e.g., `output2/`) will contain:

- `motion_detection.mp4`  
- `viewport_tracking.mp4`  
- Any intermediate frames generated during processing

---

## Troubleshooting

### 1) `ModuleNotFoundError: No module named 'imageio'` or FFmpeg errors
- Install the missing packages:
  ```bash
  pip install imageio imageio-ffmpeg
  ```
- If problems persist, try a fresh virtual environment and reinstall:
  ```bash
  python -m venv .venv
  # Activate it:
  #   Windows: .venv\Scripts\activate
  #   macOS/Linux: source .venv/bin/activate
  pip install -r requirement.txt
  pip install imageio-ffmpeg
  ```

### 2) `No such file or directory` (video path or output path)
- Double‑check the `--video` path. Use quotes if there are spaces.
- Ensure the `data/` folder contains the input video.
- Make sure the `--output` directory exists or can be created by the program. If not, create it manually:
  ```bash
  mkdir -p ./output2
  ```

### 3) `--viewport_size` format issues
- The argument must be in `WxH` with integers (e.g., `720x480`, `800x450`). No spaces.

### 4) Permission/activation issues on macOS/Linux
- If your environment isn’t active, commands may install to a different Python. Activate your venv before installing and running.

---

## Notes

- Processing at higher `--fps` or larger `--viewport_size` increases compute and memory usage.
- Input videos with unusual codecs may require a system FFmpeg install in addition to `imageio-ffmpeg`.

