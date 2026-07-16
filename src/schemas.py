"""
Pydantic schemas used for validation with image support.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional


class BoundingBox(BaseModel):
    """
    Bounding box representation with coordinates and dimensions.
    Can be initialized from array [x, y, width, height] or object format.
    """
    x: float = Field(ge=0, description="X coordinate of top-left corner")
    y: float = Field(ge=0, description="Y coordinate of top-left corner")
    width: float = Field(gt=0, description="Width of bounding box")
    height: float = Field(gt=0, description="Height of bounding box")

    @field_validator("width", "height")
    @classmethod
    def validate_dimensions(cls, value):
        """Ensure positive dimensions."""
        if value <= 0:
            raise ValueError("Width and height must be positive")
        return value

    def to_dict(self):
        """Convert to dictionary format."""
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height
        }

    def to_array(self):
        """Convert to array format [x, y, width, height]."""
        return [self.x, self.y, self.width, self.height]

    @classmethod
    def from_array(cls, bbox_array):
        """Create BoundingBox from array [x, y, width, height]."""
        if not isinstance(bbox_array, (list, tuple)) or len(bbox_array) != 4:
            raise ValueError("BBox must be array/tuple of 4 elements: [x, y, width, height]")
        return cls(x=bbox_array[0], y=bbox_array[1], width=bbox_array[2], height=bbox_array[3])


class Annotation(BaseModel):
    """
    Single annotation record with image reference and bounding box.
    """
    image_id: str = Field(description="Unique image identifier")
    annotation_id: str = Field(description="Unique annotation identifier")
    label: str = Field(description="Equipment label/class")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score 0-1")
    bbox: BoundingBox = Field(description="Bounding box coordinates")
    image_filename: Optional[str] = Field(None, description="Optional image filename reference")

    @field_validator("label")
    @classmethod
    def validate_label(cls, value):
        """Convert label to lowercase and validate non-empty."""
        if not value or not value.strip():
            raise ValueError("Label cannot be empty")
        return value.lower().strip()

    @field_validator("image_id", "annotation_id")
    @classmethod
    def validate_ids(cls, value):
        """Validate IDs are non-empty strings."""
        if not value or not str(value).strip():
            raise ValueError("ID cannot be empty")
        return str(value).strip()


class AnnotationFile(BaseModel):
    """
    Container for multiple annotations from a single source.
    """
    annotations: list[Annotation] = Field(description="List of annotations")

    def __len__(self):
        return len(self.annotations)

    def to_dict_list(self):
        """Convert to list of dictionaries."""
        return [ann.model_dump() for ann in self.annotations]


class ImageMetadata(BaseModel):
    """
    Image metadata with validation.
    """
    image_id: str = Field(description="Unique image identifier")
    file_name: str = Field(description="Image filename")
    equipment_type: str = Field(description="Type of equipment in image")
    width: int = Field(gt=0, description="Image width in pixels")
    height: int = Field(gt=0, description="Image height in pixels")

    @field_validator("file_name", "equipment_type")
    @classmethod
    def validate_strings(cls, value):
        """Validate non-empty strings."""
        if not value or not value.strip():
            raise ValueError("Field cannot be empty")
        return value.strip()


class ImageQualityReport(BaseModel):
    """
    Quality assessment report for image annotations.
    """
    image_id: str
    image_filename: str
    equipment_type: str
    image_width: int
    image_height: int
    annotation_count: int
    quality_score: float = Field(ge=0.0, le=1.0)
    status: str  # "PASS" or "FAIL"
    issues: list[str] = Field(default_factory=list)
    validation_timestamp: str
