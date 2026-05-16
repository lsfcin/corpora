import torch.nn as nn
from _typeshed import Incomplete

class ResidualConvUnit(nn.Module):
    bn: Incomplete
    groups: int
    conv1: Incomplete
    conv2: Incomplete
    bn1: Incomplete
    bn2: Incomplete
    activation: Incomplete
    skip_add: Incomplete
    def __init__(self, features, activation, bn) -> None: ...
    def forward(self, x): ...

class FeatureFusionBlock(nn.Module):
    deconv: Incomplete
    align_corners: Incomplete
    groups: int
    expand: Incomplete
    out_conv: Incomplete
    resConfUnit1: Incomplete
    resConfUnit2: Incomplete
    skip_add: Incomplete
    size: Incomplete
    def __init__(self, features, activation, deconv: bool = False, bn: bool = False, expand: bool = False, align_corners: bool = True, size=None) -> None: ...
    def forward(self, *xs, size=None): ...
