from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import delete
from database import async_session_maker


class BaseCRUD:
    model = None

    @classmethod
    async def find_one_or_none_by_id(cls, id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            plain_result = result.scalar_one_or_none()
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

    @classmethod
    async def delete(cls, presentation_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                query = delete(cls.model).filter(cls.model.id == presentation_id)
                await session.execute(query)
                await session.commit()
                return {"message": "obj deleted"}
