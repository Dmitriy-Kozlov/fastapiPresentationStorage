from fastapi import APIRouter, UploadFile, File, Form, Depends
from presentations.schemas import PresentationRead, PresentationFilter, MonthEnum
from presentations.crud import PresentationCRUD
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


@router.post("/filter", response_model=list[PresentationRead] | None)
async def get_presentation_by_filter(filter_data: PresentationFilter):
    presentation = await PresentationCRUD.find_presentation_by_filter(
        owner=filter_data.owner,
        title=filter_data.title,
        month=filter_data.month,
        year=filter_data.year
    )
    return presentation


@router.get("/download")
async def download_presentation(id: int,):
    file = await PresentationCRUD.download(id)
    return file


@router.get("/{id}", response_model=PresentationRead | None)
async def get_presentation_by_id(id: int):
    presentation = await PresentationCRUD.find_one_or_none_by_id(id)
    return presentation


@router.delete("/{id}/delete")
async def delete_presentation_by_id(id: int, user=Depends(get_current_active_user)):
    result = await PresentationCRUD.delete(id)
    return result
