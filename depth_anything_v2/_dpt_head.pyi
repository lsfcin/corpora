import torch.nn as nn
from _typeshed import Incomplete

class ConvBlock(nn.Module):
    conv_block: Incomplete
    def __init__(self, in_feature, out_feature) -> None: ...
    def forward(self, x): ...

class DPTHead(nn.Module):
    use_clstoken: Incomplete
    projects: Incomplete
    resize_layers: Incomplete
    readout_projects: Incomplete
    scratch: Incomplete
    def __init__(self, in_channels, features: int = 256, use_bn: bool = False, out_channels=[256, 512, 1024, 1024], use_clstoken: bool = False) -> None: ...
    def forward(self, out_features, patch_h, patch_w): ...
