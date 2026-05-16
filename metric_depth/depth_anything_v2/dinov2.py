# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the Apache License, Version 2.0
# found in the LICENSE file in the root directory of this source tree.

# Public API surface for DINOv2 ViT models.
# Implementation is split across:
#   _vit_helpers.py  — named_apply, BlockChunk, init helpers, feature-extraction mixin
#   _vit_core.py     — DinoVisionTransformer (constructor + forward)
#   _vit_factory.py  — vit_small/base/large/giant2, DINOv2 entry point

from ._vit_helpers import named_apply, BlockChunk, init_weights_vit_timm
from ._vit_core import DinoVisionTransformer
from ._vit_factory import vit_small, vit_base, vit_large, vit_giant2, DINOv2

__all__ = [
    "named_apply",
    "BlockChunk",
    "init_weights_vit_timm",
    "DinoVisionTransformer",
    "vit_small",
    "vit_base",
    "vit_large",
    "vit_giant2",
    "DINOv2",
]
