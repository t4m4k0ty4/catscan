from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Page(Base):
    __tablename__ = "pages"
    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str]
    selector_type: Mapped[str]
    selector: Mapped[str]
    comment: Mapped[str]
    created_at: Mapped[str] = mapped_column(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: Mapped[str] = mapped_column(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logs: Mapped[list["Log"]] = relationship(
        "Log", cascade="all, delete-orphan", back_populates="page", lazy="selectin"
    )
    news: Mapped[list["News"]] = relationship(
        "News", cascade="all, delete-orphan", back_populates="page", lazy="selectin"
    )


class Log(Base):
    __tablename__ = "logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id"))
    prev_value: Mapped[str | None]
    current_value: Mapped[str | None]
    error_message: Mapped[str | None]
    created_at: Mapped[str] = mapped_column(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    page: Mapped["Page"] = relationship("Page", back_populates="logs")


class News(Base):
    __tablename__ = "news"
    id: Mapped[int] = mapped_column(primary_key=True)
    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id"))
    title: Mapped[str | None]
    is_new_article: Mapped[bool] = mapped_column(default=True)
    description: Mapped[str | None]
    created_at: Mapped[str] = mapped_column(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    page: Mapped["Page"] = relationship("Page", back_populates="news")
