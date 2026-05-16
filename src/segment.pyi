from _typeshed import Incomplete

class Segmenter:
    segmenter: Incomplete
    results: Incomplete
    masks: Incomplete
    boxes: Incomplete
    labels: Incomplete
    scores: Incomplete
    contours: Incomplete
    def __init__(self) -> None: ...
    def show(self, image, threshold: float = 0.5) -> None: ...
    def process(self, image) -> None: ...
    def get(self): ...
