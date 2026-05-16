from ._vit_helpers import DinoVisionTransformerFeatures
from .dinov2_layers import MemEffAttention as MemEffAttention
from _typeshed import Incomplete

logger: Incomplete

class DinoVisionTransformer(DinoVisionTransformerFeatures):
    num_features: Incomplete
    num_tokens: int
    n_blocks: Incomplete
    num_heads: Incomplete
    patch_size: Incomplete
    num_register_tokens: Incomplete
    interpolate_antialias: Incomplete
    interpolate_offset: Incomplete
    patch_embed: Incomplete
    cls_token: Incomplete
    pos_embed: Incomplete
    register_tokens: Incomplete
    chunked_blocks: bool
    blocks: Incomplete
    norm: Incomplete
    head: Incomplete
    mask_token: Incomplete
    def __init__(self, img_size: int = 224, patch_size: int = 16, in_chans: int = 3, embed_dim: int = 768, depth: int = 12, num_heads: int = 12, mlp_ratio: float = 4.0, qkv_bias: bool = True, ffn_bias: bool = True, proj_bias: bool = True, drop_path_rate: float = 0.0, drop_path_uniform: bool = False, init_values=None, embed_layer=..., act_layer=..., block_fn=..., ffn_layer: str = 'mlp', block_chunks: int = 1, num_register_tokens: int = 0, interpolate_antialias: bool = False, interpolate_offset: float = 0.1) -> None: ...
    def init_weights(self) -> None: ...
    def forward(self, *args, is_training: bool = False, **kwargs): ...
