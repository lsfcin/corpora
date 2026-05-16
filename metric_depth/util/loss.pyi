from _typeshed import Incomplete
from torch import nn

class SiLogLoss(nn.Module):
    lambd: Incomplete
    def __init__(self, lambd: float = 0.5) -> None: ...
    def forward(self, pred, target, valid_mask): ...
