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
    
    def draw(self, image):
        # Draw the depth map on the image
        #result = cv2.resize(self.depth_map, (image.shape[1], image.shape[0]))
        
        result = (self.depth_map - self.depth_map.min()) / (self.depth_map.max() - self.depth_map.min()) * 255.0
        result = result.astype(np.uint8)
        result = (self.cmap(result)[:, :, :3] * 255)[:, :, ::-1].astype(np.uint8)
        
        # self.depth_map = (self.depth_map - self.depth_map.min()) / (self.depth_map.max() - self.depth_map.min())
        # self.depth_map = (self.cmap(self.depth_map) * 255).astype(np.uint8)
        # self.depth_map = cv2.cvtColor(self.depth_map, cv2.COLOR_RGBA2RGB)
        # image = cv2.addWeighted(image, 0.7, self.depth_map, 0.3, 0)
        return result