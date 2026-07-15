"""
Pydantic schemas used for validation.
"""

from pydantic import BaseModel, Field, field_validator


class BoundingBox(BaseModel):

    x: float = Field(ge=0)
    y: float = Field(ge=0)

    width: float = Field(gt=0)

    height: float = Field(gt=0)


class Annotation(BaseModel):

    image_id: str

    annotation_id: str

    label: str

    confidence: float = Field(ge=0.0, le=1.0)

    bbox: BoundingBox


    @field_validator("label")
    @classmethod
    def validate_label(cls, value):

        return value.lower()


class AnnotationFile(BaseModel):

    annotations: list[Annotation]
