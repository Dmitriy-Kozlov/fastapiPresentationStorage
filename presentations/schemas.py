from pydantic import BaseModel, Field


class PresentationBase(BaseModel):
    title: str = Field(..., description="Название презентации")
    owner: str = Field(..., description="Автор презентации")
    year: str = Field(..., description="Год презентации")


class PresentationRead(PresentationBase):
    id: int = Field(..., description="Уникальный идентификатор презентации")


class PresentationCreate(PresentationBase):
    pass
