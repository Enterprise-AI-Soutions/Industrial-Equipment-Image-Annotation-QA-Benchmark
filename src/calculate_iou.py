"""
Intersection over Union (IoU) calculation.
"""

from src.schemas import BoundingBox


def calculate_iou(box1: BoundingBox, box2: BoundingBox) -> float:
    """
    Calculate Intersection over Union.

    Returns
    -------
    float
        IoU value between 0 and 1.
    """

    x_left = max(box1.x, box2.x)
    y_top = max(box1.y, box2.y)

    x_right = min(box1.x + box1.width,
                  box2.x + box2.width)

    y_bottom = min(box1.y + box1.height,
                   box2.y + box2.height)

    if x_right <= x_left or y_bottom <= y_top:
        return 0.0

    intersection = (x_right - x_left) * (y_bottom - y_top)

    area1 = box1.width * box1.height
    area2 = box2.width * box2.height

    union = area1 + area2 - intersection

    return round(intersection / union, 3)
