# depth_anything_v2
> ← add description

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`dinov2_layers/`](dinov2_layers/CONTEXT.md) | — |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`_dpt_head.py`](_dpt_head.py) | — | `ConvBlock`, `DPTHead`, `forward`, `forward` | DepthAnythingV2: DPT decoder head — projects and fuses multi-scale ViT features into a depth map. |
| [`_vit_core.py`](_vit_core.py) | — | `DinoVisionTransformer`, `init_weights`, `forward`, `f` | Copyright (c) Meta Platforms, Inc. and affiliates. |
| [`_vit_factory.py`](_vit_factory.py) | — | `vit_small`, `vit_base`, `vit_large`, `vit_giant2`, `DINOv2` | Copyright (c) Meta Platforms, Inc. and affiliates. |
| [`_vit_helpers.py`](_vit_helpers.py) | — | `named_apply`, `BlockChunk`, `init_weights_vit_timm`, `DinoVisionTransformerFeatures`, `forward` | Copyright (c) Meta Platforms, Inc. and affiliates. |
| [`dinov2.py`](dinov2.py) | [`dinov2.pyi`](dinov2.pyi) | — | Copyright (c) Meta Platforms, Inc. and affiliates. |
| [`dpt.py`](dpt.py) | [`dpt.pyi`](dpt.pyi) | `DepthAnythingV2`, `forward`, `infer_image`, `image2tensor` | DepthAnythingV2 DPT model: encoder-decoder architecture for monocular depth estimation |
| [`util/blocks.py`](util/blocks.py) | [`util/blocks.pyi`](util/blocks.pyi) | `ResidualConvUnit`, `FeatureFusionBlock`, `forward`, `forward` | DPT building blocks: scratch layers, residual conv blocks, feature fusion, and head |
| [`util/transform.py`](util/transform.py) | [`util/transform.pyi`](util/transform.pyi) | `Resize`, `NormalizeImage`, `PrepareForNet`, `constrain_to_multiple_of`, `get_size` | Image pre-processing transforms: resize, normalize, and prepare for DepthAnythingV2 |
<!-- routing:end -->
