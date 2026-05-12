# Corpora

Real-time 3D computer vision research pipeline. Combines monocular depth estimation, human pose estimation, and segmentation from a live webcam feed to produce 3D spatial understanding (bounding boxes, 6-DoF pose, point clouds).

## Stack

Python · PyTorch · OpenCV · DepthAnythingV2 · MediaPipe

## Architecture

```
Webcam → Input → [DepthEstimator | PoseEstimator | Segmenter] → Geometry → Window
```

## File Map

**Custom pipeline (`src/`)**

- `src/depth.py` — `DepthEstimator`: wraps DepthAnythingV2; produces per-frame depth maps
- `src/hpe.py` — `PoseEstimator`: human pose estimation (landmark detection)
- `src/segment.py` — `Segmenter`: instance/semantic segmentation
- `src/input.py` — `Input`: webcam capture and frame normalization
- `src/window.py` — `Window`: OpenCV display loop and visualization overlay
- `src/geometry.py` — `Geometry`: 3D reconstruction helpers (depth → point cloud, 3D bounds)
- `src/box3d.py` — 3D bounding box representation and projection utilities
- `src/pose6dof.py` — 6-DoF pose estimation from depth + landmarks
- `src/visualizer3d.py` — optional 3D visualizer (currently disabled in main.py)
- `main.py` — entry point; assembles the pipeline and runs the webcam loop

**Third-party research code (do not edit)**

- `depth_anything_v2/` — DepthAnythingV2 model (DINOv2 backbone + DPT head)
- `metric_depth/` — metric depth variant with dataset loaders and training scripts

## Working Rules

- `depth_anything_v2/` and `metric_depth/` are upstream research code — patch by subclassing or wrapping, not by editing directly.
- Model checkpoints are not committed; download separately per `requirements.txt` notes.
- `src/visualizer3d.py` is disabled — re-enable cautiously, it has heavy 3D rendering deps.
