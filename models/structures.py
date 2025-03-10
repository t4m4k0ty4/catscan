from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_serializer


class SelectorType(StrEnum):
    XPATH = "xpath"
    REGEX = "regex"


class PageBase(BaseModel):
    link: HttpUrl = Field(title="Ссылка на страницу новостного ресура")
    selector_type: SelectorType = Field(title="Тип селектора отслеживаемого элемента")
    selector: str = Field(title="Строка селектора")
    comment: str = Field(title="Комментарий")

    @field_serializer("link")
    def serialize_link(self, value: HttpUrl) -> str:
        return str(value)


class Page(PageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(title="Уникальный идентификатор страницы")
    created_at: datetime = Field(title="Дата создания страницы")
    updated_at: datetime = Field(title="Дата последнего обновления страницы")


class Log(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(title="Уникальный идентификатор лога")
    page_id: int = Field(title="Уникальный идентификатор страницы")
    prev_value: str | None = Field(title="Предыдущее значение")
    current_value: str | None = Field(title="Текущее значение")
    error_message: str | None = Field(title="Сообщение об ошибке")
    created_at: datetime = Field(title="Дата создания лога")


class News(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(description="Уникальный идентификатор новости")
    page_id: int = Field(description="Уникальный идентификатор страницы")
    title: str | None = Field(description="Заголовок новости")
    is_new_article: bool | None = Field(default=True, description="Признак новой статьи")
    description: str | None = Field(description="Описание новости")
    created_at: datetime = Field(description="Дата создания новости")
