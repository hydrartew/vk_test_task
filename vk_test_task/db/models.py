from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy import String, Text

from vk_test_task.db.base import Base


class RawPostsTable(Base):
    __tablename__ = "raw_users_by_posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(128), nullable=False)
    body = Column(Text, nullable=False)


class TopUsersTable(Base):
    __tablename__ = "top_users_by_posts"

    user_id = Column(Integer, primary_key=True)
    posts_cnt = Column(Integer, nullable=False)
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
