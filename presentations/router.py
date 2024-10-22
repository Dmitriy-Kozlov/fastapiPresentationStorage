from fastapi import APIRouter, UploadFile, File, Form, Depends
from presentations.schemas import PresentationRead
from presentations.crud import PresentationCRUD, MonthEnum
from users.router import get_current_active_user

router = APIRouter(
    prefix="/presentations",
    tags=["presentations"]
)


@router.post("/add", response_model=PresentationRead)
async def add_presentation(
        user=Depends(get_current_active_user),
        title: str = Form(...),
        owner: str = Form(...),
        year: int = Form(...),
        month: MonthEnum = Form(...),
        file: UploadFile = File(...)
                            ):
    presentation = await PresentationCRUD.add(title=title, owner=owner, year=year, month=month, file=file)
    return presentation


@router.get("/all", response_model=list[PresentationRead])
async def get_all_presentations():
    presentations = await PresentationCRUD.find_all()
    return presentations


@router.get("/filter", response_model=list[PresentationRead] | None)
async def get_presentation_by_filter(owner: str = None, title: str = None, month: MonthEnum = None, year: int = None):
    presentation = await PresentationCRUD.find_presentation_by_filter(owner=owner, title=title, month=month, year=year)
    return presentation


@router.get("/download")
async def download_presentation(presentation_id: int,):
    file = await PresentationCRUD.download(presentation_id)
    return file


@router.get("/{id}", response_model=PresentationRead | None)
async def get_presentation_by_id(id: int):
    presentation = await PresentationCRUD.find_one_or_none_by_id(id)
    return presentation


@router.delete("/{id}/delete")
async def delete_presentation_by_id(id: int):
    result = await PresentationCRUD.delete(id)
    return result
