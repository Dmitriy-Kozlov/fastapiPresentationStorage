from enum import Enum

from pydantic import BaseModel, Field


class MonthEnum(str, Enum):
    # nill = ""
    january = "Январь"
    february = "Февраль"
    march = "Март"
    april = "Апрель"
    may = "Май"
    june = "Июнь"
    july = "Июль"
    august = "Август"
    september = "Сентябрь"
    october = "Октябрь"
    november = "Ноябрь"
    december = "Декабрь"


class PresentationBase(BaseModel):
    title: str = Field(..., description="Название презентации")
    owner: str = Field(..., description="Автор презентации")
    month: str = Field(..., description="Месяц презентации")
    year: int = Field(gt=2000, description="Год презентации (должен быть больше 2000)")


class PresentationRead(PresentationBase):
    id: int = Field(..., description="Уникальный идентификатор презентации")


class PresentationCreate(PresentationBase):
    pass


class PresentationFilter(BaseModel):
    owner: str | None = None
    title: str | None = None
    month: MonthEnum | None = None
    year: int | None = None