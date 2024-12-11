"""Models and api module."""
import uuid
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (DeclarativeBase, Mapped,
                            mapped_column)
from datetime import datetime


class Base(DeclarativeBase):
    """Base class for declarative models."""

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()

class Schedule(Base):
    __tablename__ = 'schedules'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
    timestamp: Mapped[datetime] = mapped_column()
    task_name: Mapped[str] = mapped_column()
    task_description: Mapped[str] = mapped_column()