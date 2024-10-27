import shutil
import os
import glob
from sqlalchemy import delete
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.future import select
from starlette.responses import FileResponse

from database import async_session_maker
from presentations.models import Presentation
from base.crud import BaseCRUD
from presentations.schemas import PresentationCreate


class PresentationCRUD(BaseCRUD):
    model = Presentation

    @classmethod
    async def find_presentation_by_filter(cls, **filter):
        async with async_session_maker() as session:
            filters = dict(**{k:v for k, v in filter.items() if v is not None})
            title = filters.pop("title", None)
            query = select(cls.model).filter_by(**filters)
            if title is not None:
                query = query.filter(Presentation.title.ilike(f"%{title}%"))
            result = await session.execute(query)
            plain_result = result.scalars().all()
            return plain_result

    @classmethod
    async def add(cls, title, owner, year, month, file):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    presentation_data = PresentationCreate(title=title, owner=owner, month=month, year=year)
                except ValidationError as e:
                    raise HTTPException(status_code=400, detail=e.errors())
                file_extension = file.filename.split(".")[-1]
                new_instance = cls.model(title=title, owner=owner, month=month, year=year, extension=file_extension)
                session.add(new_instance)
                await session.flush()
                os.makedirs(f"media/presentations", exist_ok=True)
                with open(f"media/presentations/{new_instance.id}.{file_extension}", "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

    @classmethod
    async def download(cls, presentation_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    query = select(Presentation).filter_by(id=presentation_id)
                    result = await session.execute(query)
                    presentation = result.scalars().one()
                    filename = f"{presentation.id}.{presentation.extension}"
                    path = f"media/presentations/{filename}"
                    return FileResponse(path, media_type='application/octet-stream',
                                        filename=f"{presentation.owner}-{presentation.year}-{presentation.month}.{presentation.extension}")
                except NoResultFound:
                    raise HTTPException(status_code=404, detail="Presentation not found")

    @classmethod
    async def delete(cls, presentation_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                query = delete(cls.model).filter(cls.model.id == presentation_id)
                await session.execute(query)
                await session.commit()
                file_pattern = f"media/presentations/{presentation_id}.*"
                files_to_delete = glob.glob(file_pattern)
                if not files_to_delete:
                    raise FileNotFoundError(f"No files found for presentation ID {presentation_id}")
                for file_path in files_to_delete:
                    os.remove(file_path)
                return {"message": "obj deleted"}
