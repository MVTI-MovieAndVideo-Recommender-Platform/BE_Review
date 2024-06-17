from model import Base
from sqlalchemy import CHAR, DECIMAL, Boolean, DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class RatingORM(Base):
    __tablename__ = "rating"

    rating_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    user_id: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    media_id: Mapped[int] = mapped_column(Integer, nullable=False)
    rating: Mapped[float] = mapped_column(DECIMAL(2, 1), nullable=False)
    last_update: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    is_delete: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class PreferenceORM(Base):
    __tablename__ = "preference"

    preference_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    user_id: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    media_id: Mapped[int] = mapped_column(Integer, nullable=False)
    last_update: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    is_delete: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
