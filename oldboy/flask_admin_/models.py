import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    ForeignKey, Column, Integer, String, Text, DateTime, UniqueConstraint, Index
)

Base = declarative_base()


class UserInfo(Base):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(32), index=True, nullable=False)
    email = Column(String(32), unique=True, nullable=True)
    create_time = Column(DateTime, default=datetime.datetime.now)
    introduction = Column(Text, nullable=True)

    __tablename__ = 'userinfo'
    __table_args__ = (
        UniqueConstraint('id', 'name', name='uix_id_name'),
        Index('ix_id_name', 'name', 'email'),  # 索引
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
