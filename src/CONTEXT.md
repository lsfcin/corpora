# src
> ← add description

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`box3d.py`](box3d.py) | [`box3d.pyi`](box3d.pyi) | `Box3D` | Box3D: 3D bounding box combining physical dimensions and 6-DOF pose |
| [`depth.py`](depth.py) | [`depth.pyi`](depth.pyi) | `DepthEstimator`, `process`, `get`, `show` | DepthEstimator: wraps DepthAnythingV2 to produce per-frame depth maps from RGB |
| [`geometry.py`](geometry.py) | [`geometry.pyi`](geometry.pyi) | `Geometry`, `process`, `create_box`, `show` | Geometry: lifts 2D detections to 3D boxes using depth maps and camera intrinsics |
| [`hpe.py`](hpe.py) | [`hpe.pyi`](hpe.pyi) | `PoseEstimator`, `process`, `get`, `show`, `extract_gaze_and_head` | hpe stands for human pose estimator |
| [`input.py`](input.py) | [`input.pyi`](input.pyi) | `Input` | Input: threaded mouse and keyboard listener for real-time interaction |
| [`pose6dof.py`](pose6dof.py) | [`pose6dof.pyi`](pose6dof.pyi) | `Pose6DOF` | Pose6DOF: 6-degree-of-freedom pose with position and direction vectors |
| [`segment.py`](segment.py) | [`segment.pyi`](segment.pyi) | `Segmenter`, `show`, `process`, `get` | Segmenter: YOLO11-seg instance segmentation wrapper producing masks and bounding boxes |
| [`visualizer3d.py`](visualizer3d.py) | [`visualizer3d.pyi`](visualizer3d.pyi) | `Cube`, `Visualizer3D`, `mouse_callback`, `mouse_callback`, `show` | Visualizer3D: OpenCV overlay renderer for 3D bounding cube projections |
| [`window.py`](window.py) | [`window.pyi`](window.pyi) | `Window`, `process`, `show` | Window: tracks the active OS window to associate detections with the foreground application |
<!-- routing:end -->
