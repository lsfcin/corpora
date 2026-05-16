from _typeshed import Incomplete

class Cube:
    top_left_front: Incomplete
    bottom_right_back: Incomplete
    points: Incomplete
    edges: Incomplete
    def __init__(self, top_left_front, bottom_right_back) -> None: ...

class Visualizer3D:
    cube: Incomplete
    focal_length: int
    center: Incomplete
    camera_matrix: Incomplete
    rotation_vector: Incomplete
    translation_vector: Incomplete
    def __init__(self) -> None: ...
    def mouse_callback(self, event, x, y, flags, param) -> None: ...
    def show(self, cubes, colors) -> None: ...

def mouse_callback(event, x, y, flags, param) -> None: ...
