from sqlalchemy import select
from typing import List

from app.services.database.models import Statistic
from app.services.database.repository.base_repository import BaseRepository


class StatisticRepository(BaseRepository):
    async def get_all_stats(self, offset: int, limit: int):
        stmt = select(Statistic).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create_stat(self, mio_values: List[int], user_id: int, status: bool):
        stat = Statistic(mio_values=mio_values, user_id=user_id, status=status)
        self.db.add(stat)
        await self.db.commit()
