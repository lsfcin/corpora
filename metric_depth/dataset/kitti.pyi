from _typeshed import Incomplete
from torch.utils.data import Dataset

class KITTI(Dataset):
    mode: Incomplete
    size: Incomplete
    filelist: Incomplete
    transform: Incomplete
    def __init__(self, filelist_path, mode, size=(518, 518)) -> None: ...
    def __getitem__(self, item): ...
    def __len__(self) -> int: ...
