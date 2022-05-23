import datetime
import pytz

from sqlalchemy import select, extract, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import noload, joinedload
from typing import Union

from app.services.database.models import User, Statistic
from app.services.database.repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    async def get_user(self, user_id: str) -> Union[User, None]:
        try:
            stmt = select(User).options(noload(User.statistics)).where(User.id == user_id)
            result = await self.db.execute(stmt)
            return result.scalar().one()
        except NoResultFound:
            return None

    async def create_user(self, vk_login: str, vk_password: str) -> Union[User, None]:
        user = User(vk_login=vk_login, vk_password=vk_password)
        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except IntegrityError:
            await self.db.rollback()
            return None

    async def get_users(self):
        today = datetime.datetime.now(tz=pytz.timezone("Europe/Moscow"))
        stmt = select(
            User
        ).options(
            joinedload(
                User.statistics
            )
        ).filter(
            extract("day", Statistic.time_stamp) == today.day
        )
        result = await self.db.execute(stmt)
        return result.scalar().all()

    async def update_user_smoke_count(self, user_id: int, no_smoke_count: int):
        stmt = update(User).where(User.id == user_id).values({User.no_smoke_count: no_smoke_count})
        await self.db.execute(stmt)

