from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from database import async_session_maker
from presentations.models import Presentation


class PresentationCRUD:
    model = Presentation

    @classmethod
    async def find_one_or_none_by_id(cls, id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            plain_result = result.scalar_one_or_none()
            return plain_result

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
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            plain_result = result.scalars().all()
            return plain_result

    @classmethod
    async def add(cls, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance
