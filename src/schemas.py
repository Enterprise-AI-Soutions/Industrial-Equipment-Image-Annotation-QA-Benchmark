from pydantic import BaseModel, Field


class Annotation(BaseModel):

    image_id: str

    label: str

    bbox: list[int] = Field(min_length=4, max_length=4)

    annotator: str
