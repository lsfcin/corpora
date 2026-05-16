import torch.nn as nn
from ._dpt_head import ConvBlock as ConvBlock, DPTHead as DPTHead, _make_fusion_block as _make_fusion_block
from _typeshed import Incomplete

__all__ = ['DPTHead', 'ConvBlock', '_make_fusion_block', 'DepthAnythingV2']

class DepthAnythingV2(nn.Module):
    intermediate_layer_idx: Incomplete
    max_depth: Incomplete
    encoder: Incomplete
    pretrained: Incomplete
    depth_head: Incomplete
    def __init__(self, encoder: str = 'vitl', features: int = 256, out_channels=[256, 512, 1024, 1024], use_bn: bool = False, use_clstoken: bool = False, max_depth: float = 20.0) -> None: ...
    def forward(self, x): ...
    def infer_image(self, raw_image, input_size: int = 518): ...
    def image2tensor(self, raw_image, input_size: int = 518): ...
