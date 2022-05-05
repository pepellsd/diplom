from sqlalchemy import select

from app.services.database.models import Statistic
from app.services.database.repository.base_repository import BaseRepository


class StatisticRepository(BaseRepository):
    async def get_all_stats(self, offset: int, limit: int):
        stmt = select(Statistic).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create_stat(self, mio_value: int, user_id: int):
        stat = Statistic(mio_value=mio_value, user_id=user_id)
        self.db.add(stat)
        await self.db.commit()
