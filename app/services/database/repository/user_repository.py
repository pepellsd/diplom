from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import noload
from typing import Union

from app.services.database.models import User
from app.services.database.repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    async def get_user(self, user_id: str) -> Union[User, None]:
        try:
            stmt = select(User).options(noload(User.statistic)).where(User.id == user_id)
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
