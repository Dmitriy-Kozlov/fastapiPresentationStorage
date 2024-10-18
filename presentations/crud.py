from sqlalchemy.future import select
from database import async_session_maker
from presentations.models import Presentation
from base.crud import BaseCRUD


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
