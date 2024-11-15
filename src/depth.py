import cv2
import torch
import matplotlib
import numpy as np
from depth_anything_v2.dpt import DepthAnythingV2

class DepthEstimator:
    def __init__(self):
        DEVICE = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'

        depth_anything_configs = {
            'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
            'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
            'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
            'vitg': {'encoder': 'vitg', 'features': 384, 'out_channels': [1536, 1536, 1536, 1536]}
        }

        encoder = 'vits' # or 'vits', 'vitb', 'vitg'

        # depth
        self.depth_estimator = DepthAnythingV2(**depth_anything_configs[encoder])
        self.depth_estimator.load_state_dict(torch.load(f'rsc/depth_anything_v2_{encoder}.pth', map_location='cpu'))
        self.depth_estimator = self.depth_estimator.to(DEVICE).eval()

        self.cmap = matplotlib.colormaps.get_cmap('Spectral_r')

    def process(self, image):
        # HxW raw depth map in numpy
        self.depth_map = self.depth_estimator.infer_image(image) 

    def get(self):
        return self.depth_map
    
    # Draw the depth map on the image
    def draw(self, output_image):        
        normalized_depth_map = (self.depth_map - self.depth_map.min()) / (self.depth_map.max() - self.depth_map.min()) * 255.0
        normalized_depth_map = normalized_depth_map.astype(np.uint8)
        normalized_depth_map = (self.cmap(normalized_depth_map)[:, :, :3] * 255)[:, :, ::-1].astype(np.uint8)
        output_image.data = normalized_depth_map.data