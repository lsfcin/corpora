# metric_depth
> ← add description

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`depth_anything_v2/`](depth_anything_v2/CONTEXT.md) | — |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`README.md`](README.md) | — | — | Depth Anything V2 for Metric Depth Estimation |
| [`_train_loop.py`](_train_loop.py) | [`_train_loop.pyi`](_train_loop.pyi) | `run_train_epoch`, `run_eval_epoch`, `reduce_eval_results`, `log_and_save` | Training loop and evaluation helpers for DepthAnythingV2 metric depth fine-tuning. |
| [`dataset/_min_size.py`](dataset/_min_size.py) | [`dataset/_min_size.pyi`](dataset/_min_size.pyi) | `apply_min_size` | Dataset transform helper: apply_min_size — upscale sample to a minimum resolution. |
| [`dataset/_resize.py`](dataset/_resize.py) | [`dataset/_resize.pyi`](dataset/_resize.pyi) | `Resize`, `constrain_to_multiple_of`, `get_size` | Dataset transforms: Resize transform for metric depth training. |
| [`dataset/hypersim.py`](dataset/hypersim.py) | [`dataset/hypersim.pyi`](dataset/hypersim.pyi) | `hypersim_distance_to_depth`, `Hypersim` | HyperSim dataset loader: reads HDF5 depth and RGB for metric depth fine-tuning |
| [`dataset/kitti.py`](dataset/kitti.py) | [`dataset/kitti.pyi`](dataset/kitti.pyi) | `KITTI` | KITTI dataset loader: reads stereo depth and RGB for metric depth fine-tuning |
| [`dataset/transform.py`](dataset/transform.py) | [`dataset/transform.pyi`](dataset/transform.pyi) | `NormalizeImage`, `PrepareForNet`, `Crop` | Dataset transforms: Resize, NormalizeImage, PrepareForNet, Crop for metric depth training |
| [`dataset/vkitti2.py`](dataset/vkitti2.py) | [`dataset/vkitti2.pyi`](dataset/vkitti2.pyi) | `VKITTI2` | Virtual KITTI 2 dataset loader: reads synthetic depth and RGB for metric depth fine-tuning |
| [`depth_to_pointcloud.py`](depth_to_pointcloud.py) | [`depth_to_pointcloud.pyi`](depth_to_pointcloud.pyi) | `main` | Depth-to-point-cloud: back-projects metric depth maps to colored 3D PLY point clouds |
| [`dist_train.sh`](dist_train.sh) | — | — | ← add first-line comment |
| [`run.py`](run.py) | [`run.pyi`](run.pyi) | — | Inference script: runs DepthAnythingV2 metric depth on images, video, or live camera |
| [`train.py`](train.py) | [`train.pyi`](train.pyi) | `main` | Training script: fine-tunes DepthAnythingV2 on HyperSim/KITTI/vKITTI2 for metric depth |
| [`util/dist_helper.py`](util/dist_helper.py) | [`util/dist_helper.pyi`](util/dist_helper.pyi) | `setup_distributed` | Distributed training helper: sets up PyTorch DDP and queries GPU count via CUDA |
| [`util/loss.py`](util/loss.py) | [`util/loss.pyi`](util/loss.pyi) | `SiLogLoss`, `forward` | SiLogLoss: scale-invariant logarithmic loss for metric depth regression |
| [`util/metric.py`](util/metric.py) | [`util/metric.pyi`](util/metric.pyi) | `eval_depth` | Depth evaluation metrics: Abs-Rel, Sq-Rel, RMSE, delta thresholds for metric depth |
| [`util/utils.py`](util/utils.py) | [`util/utils.pyi`](util/utils.pyi) | `init_log` | Training utilities: logging setup, seed fixing, distributed gather, and checkpoint helpers |
<!-- routing:end -->
