from datetime import datetime

from sqlalchemy import String, BigInteger, DateTime, Integer
from sqlalchemy import Column, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from app.services.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    vk_login = Column(String, index=True)
    vk_password = Column(String, nullable=False)
    statistics = relationship('Statistic', passive_deletes=True)

    __table_args__ = (UniqueConstraint('vk_login', 'vk_password'))

    def __str__(self):
        return self.vk_login


class Statistic(Base):
    __tablename__ = "statistics"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    time_stamp = Column(DateTime, default=datetime.utcnow())
    mio_value = Column(Integer)

    def __str__(self):
        return self.mio_value
