import open3d as o3d
import numpy as np
import hashlib

# Define a list of 16 different colors
colors_set = [
    [255, 0, 0], 
    [0, 255, 0], 
    [0, 0, 255],
    [255, 255, 0], 
    [0, 255, 255], 
    [255, 0, 255],
    [128, 0, 0], 
    [0, 128, 0], 
    [0, 0, 128],
    [128, 128, 0], 
    [0, 128, 128], 
    [128, 0, 128],
    [64, 0, 0], 
    [0, 64, 0], 
    [0, 0, 64],
    [64, 64, 0]
]

class Box:
    def __init__(self, center, dimensions, label):

        self.center = center
        self.previous_center = np.array([0, 0, 0])

        self.dimensions = dimensions
        self.previous_dimensions = np.array([1, 1, 1])

        self.label = label

        points = np.array([
            [-0.5,  0.5, -0.5],
            [-0.5, -0.5, -0.5],
            [ 0.5, -0.5, -0.5],
            [ 0.5,  0.5, -0.5],
            [-0.5,  0.5,  0.5],
            [-0.5, -0.5,  0.5],
            [ 0.5, -0.5,  0.5],
            [ 0.5,  0.5,  0.5]])
        
        lines = [
            [0, 1], [1, 2], [2, 3], [0, 3],
            [4, 5], [5, 6], [6, 7], [4, 7],
            [0, 4], [1, 5], [2, 6], [3, 7]]
        
        color = self.get_color(self.label)
        colors = [color for _ in range(len(lines))]
        
        self.line_set = o3d.geometry.LineSet()
        self.line_set.points = o3d.utility.Vector3dVector(points)
        self.line_set.lines = o3d.utility.Vector2iVector(lines)
        self.line_set.colors = o3d.utility.Vector3dVector(colors)

        self.update(center, dimensions)

    def get_color(self, label):
        hash_object = hashlib.sha256(label.encode())
        color_id = int(hash_object.hexdigest(), 16) % 16
        color = colors_set[color_id]
        return color
    
    def update(self, center, dimensions):
        
        self.previous_center = self.center
        self.center = center

        self.previous_dimensions = self.dimensions
        self.dimensions = dimensions

        translation = center - self.previous_center
        scale = dimensions / self.previous_dimensions
        
        self.line_set.translate(translation)
        self.line_set.points = o3d.utility.Vector3dVector(
            np.asarray(self.line_set.points) * scale )    