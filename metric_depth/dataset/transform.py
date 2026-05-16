# Dataset transforms: Resize, NormalizeImage, PrepareForNet, Crop for metric depth training
# Resize and apply_min_size are implemented in _resize.py / _min_size.py.
import numpy as np

from ._min_size import apply_min_size
from ._resize import Resize


class NormalizeImage(object):
    """Normlize image by given mean and std.
    """

    def __init__(self, mean, std):
        self.__mean = mean
        self.__std = std

    def __call__(self, sample):
        sample["image"] = (sample["image"] - self.__mean) / self.__std

        return sample


class PrepareForNet(object):
    """Prepare sample for usage as network input.
    """

    def __init__(self):
        pass

    def __call__(self, sample):
        image = np.transpose(sample["image"], (2, 0, 1))
        sample["image"] = np.ascontiguousarray(image).astype(np.float32)

        if "mask" in sample:
            sample["mask"] = sample["mask"].astype(np.float32)
            sample["mask"] = np.ascontiguousarray(sample["mask"])

        if "depth" in sample:
            depth = sample["depth"].astype(np.float32)
            sample["depth"] = np.ascontiguousarray(depth)

        if "semseg_mask" in sample:
            sample["semseg_mask"] = sample["semseg_mask"].astype(np.float32)
            sample["semseg_mask"] = np.ascontiguousarray(sample["semseg_mask"])

        return sample


class Crop(object):
    """Crop sample for batch-wise training. Image is of shape CxHxW
    """

    def __init__(self, size):
        if isinstance(size, int):
            self.size = (size, size)
        else:
            self.size = size

    def __call__(self, sample):
        h, w = sample['image'].shape[-2:]
        assert h >= self.size[0] and w >= self.size[1], 'Wrong size'

        h_start = np.random.randint(0, h - self.size[0] + 1)
        w_start = np.random.randint(0, w - self.size[1] + 1)
        h_end = h_start + self.size[0]
        w_end = w_start + self.size[1]

        sample['image'] = sample['image'][:, h_start: h_end, w_start: w_end]

        if "depth" in sample:
            sample["depth"] = sample["depth"][h_start: h_end, w_start: w_end]

        if "mask" in sample:
            sample["mask"] = sample["mask"][h_start: h_end, w_start: w_end]

        if "semseg_mask" in sample:
            sample["semseg_mask"] = sample["semseg_mask"][h_start: h_end, w_start: w_end]

        return sample


__all__ = ["apply_min_size", "Resize", "NormalizeImage", "PrepareForNet", "Crop"]
