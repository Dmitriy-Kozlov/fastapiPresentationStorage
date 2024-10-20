from pydantic import BaseModel, Field
from typing import Literal


class PresentationBase(BaseModel):
    title: str = Field(..., description="Название презентации")
    owner: str = Field(..., description="Автор презентации")
    month: str = Field(..., description="Месяц презентации")
    year: int = Field(gt=2000, description="Год презентации (должен быть больше 2000)")


class PresentationRead(PresentationBase):
    id: int = Field(..., description="Уникальный идентификатор презентации")


class PresentationCreate(PresentationBase):
    pass
