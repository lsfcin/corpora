from _typeshed import Incomplete

class PoseEstimator:
    mp_body_pose: Incomplete
    mp_face_mesh: Incomplete
    mp_drawing: Incomplete
    body_pose: Incomplete
    face_mesh: Incomplete
    gaze: Incomplete
    head: Incomplete
    def __init__(self) -> None: ...
    body_results: Incomplete
    face_results: Incomplete
    def process(self, image_rgb, print_elapsed_time: bool = False) -> None: ...
    def get(self): ...
    def show(self, image) -> None: ...
    def extract_gaze_and_head(self, face_results) -> None: ...
