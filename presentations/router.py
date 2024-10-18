from fastapi import APIRouter, Body
from presentations.schemas import PresentationRead, PresentationCreate
from presentations.crud import PresentationCRUD
from typing import Union


router = APIRouter(
    prefix="/presentations",
    tags=["presentations"]
)


@router.post("/add", response_model=PresentationRead)
async def add_presentation(presentation_data: PresentationCreate):
    presentation = await PresentationCRUD.add(
        title=presentation_data.title,
        owner=presentation_data.owner,
        year=presentation_data.year,
    )
    return presentation


@router.get("/all", response_model=list[PresentationRead])
async def get_all_presentations():
    presentations = await PresentationCRUD.find_all()
    return presentations


@router.get("/filter", response_model=list[PresentationRead] | None)
async def get_presentation_by_filter(owner: str = None, title: str = None, year: str = None):
    presentation = await PresentationCRUD.find_presentation_by_filter(owner=owner, title=title, year=year)
    return presentation


@router.get("/{id}", response_model=PresentationRead | None)
async def get_presentation_by_id(id: int):
    presentation = await PresentationCRUD.find_one_or_none_by_id(id)
    return presentation