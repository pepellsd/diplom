import pytz
from datetime import datetime

from sqlalchemy import String, BigInteger, DateTime, Integer, Boolean
from sqlalchemy import Column, UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from app.services.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    vk_login = Column(String, nullable=False, index=True)
    vk_password = Column(String, nullable=False)
    no_smoke_count = Column(Integer, default=0)
    statistics = relationship('Statistic', cascade='all,delete', passive_deletes=True)

    __table_args__ = (UniqueConstraint('vk_login', 'vk_password'),)

    def __str__(self):
        return self.vk_login


class Statistic(Base):
    __tablename__ = "statistics"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    time_stamp = Column(DateTime, default=datetime.now(tz=pytz.timezone("Europe/Moscow")))
    mio_values = Column(ARRAY(Integer))
    status = Column(Boolean)

    def __str__(self):
        return f"{self.user_id}: {self.status}"
