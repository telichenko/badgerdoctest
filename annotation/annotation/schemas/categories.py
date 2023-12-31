from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, validator

from annotation.errors import CheckFieldError


class CategoryTypeSchema(str, Enum):
    box = "box"
    link = "link"
    segmentation = "segmentation"
    document = "document"
    document_link = "document_link"


class CategoryDataAttributeNames(str, Enum):
    taxonomy_id: str = "taxonomy_id"
    taxonomy_version: Optional[str] = "taxonomy_version"

    @classmethod
    def validate_schema(cls, schema: dict) -> bool:
        if not schema:
            return False

        for attr in schema:
            if attr not in cls.__members__.keys():
                return False

        if not schema.get("taxonomy_id"):
            return False
        return True


class CategoryBaseSchema(BaseModel):
    name: str = Field(..., example="Title")
    parent: Optional[str] = Field(None, example="null")
    metadata: Optional[dict] = Field(None, example={"color": "blue"})
    type: CategoryTypeSchema = Field(..., example=CategoryTypeSchema.box)
    editor: Optional[str] = Field(None, example="http://editor/")
    data_attributes: Optional[List[dict]] = Field(
        None, example=[{"attr_1": "value_1"}, {"attr_2": "value_2"}]
    )


class CategoryInputSchema(CategoryBaseSchema):
    id: Optional[str] = Field(
        None,
        example="my_category",
        description="If id is not provided, generates it as a UUID.",
    )

    @validator("id")
    def alphanumeric_validator(cls, value):
        if value and not value.replace("_", "").isalnum():
            raise CheckFieldError("Category id must be alphanumeric.")
        return value


class SubCategoriesOutSchema(BaseModel):
    id: str = Field(..., example="123")


class CategoryORMSchema(CategoryInputSchema):
    metadata: Optional[dict] = Field(
        None, example={"color": "blue"}, alias="metadata_"
    )

    class Config:
        orm_mode = True


class CategoryResponseSchema(CategoryInputSchema):
    parents: Optional[List[dict]] = Field()
    is_leaf: Optional[bool] = Field()

    class Config:
        allow_population_by_field_name = True
