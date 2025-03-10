from pydantic import BaseModel, Field, HttpUrl, field_serializer

from .structures import Page


class DeletePageResponse(BaseModel):
    message: str = Field(title="Сообщение об успешном удалении страницы")
    page: Page = Field(title="Удаленный объект страницы")


class PageDataRequest(BaseModel):
    link: HttpUrl = Field(title="Ссылка на страницу новостного ресура")
    selector_type: str = Field(title="Тип селектора отслеживаемого элемента")
    selector: str = Field(title="Строка селектора")
    comment: str | None = Field(title="Комментарий")

    @field_serializer("link")
    def serialize_link(self, value: HttpUrl) -> str:
        return str(value)
