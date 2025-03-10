import logging
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import delete, select, update

from db.models import Page
from models.interface import PageDataRequest

from .dependecies import SessionDep

templates = Jinja2Templates(directory="templates")

admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

logger = logging.getLogger(__name__)


@admin_router.get("/pages")
async def admin_pages(request: Request, session: SessionDep):
    db = session
    pages = await db.execute(select(Page))
    pages = pages.scalars().all()
    return templates.TemplateResponse("pages/pages.html", {"request": request, "pages": pages})


@admin_router.get("/pages/new")
async def new_page(request: Request):
    return templates.TemplateResponse("pages/new_page.html", {"request": request})


@admin_router.post("/pages")
async def create_page_form(request: Annotated[PageDataRequest, Form()], session: SessionDep):
    # Создаем новый объект Page на основе данных из запроса
    page_data = request.model_dump()
    page = Page(**page_data)

    # Явно задаем пустые списки для отношений
    page.logs = []
    page.news = []
    logger.debug(f"Перед добавлением: logs={page.logs}, news={page.news}")

    # Добавляем объект в сессию
    session.add(page)
    await session.flush()  # Сохраняем объект в БД, но не коммитим транзакцию
    await session.commit()  # Фиксируем изменения
    await session.refresh(page)  # Обновляем объект из БД
    logger.debug(f"После фиксации: logs={page.logs}, news={page.news}")
    return RedirectResponse(url="/admin/pages", status_code=303)


@admin_router.get("/pages/{id}/edit")
async def edit_page(id: int, request: Request, session: SessionDep):
    db = session
    page = await db.execute(select(Page).where(Page.id == id))
    page = page.scalars().first()
    return templates.TemplateResponse("pages/edit_page.html", {"request": request, "page": page})


@admin_router.post("/pages/{id}/update")
async def update_page(id: int, request: Annotated[PageDataRequest, Form()], session: SessionDep):
    db = session
    await db.execute(update(Page).where(Page.id == id).values(**request.model_dump()))
    await db.commit()
    return RedirectResponse(url="/admin/pages", status_code=303)


@admin_router.post("/pages/{id}/delete")
async def delete_page_form(id: int, session: SessionDep, method: Annotated[str, Form()] = None):
    db = session
    try:
        await db.execute(delete(Page).where(Page.id == id))
        await db.commit()
        return RedirectResponse(url="/admin/pages", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@admin_router.delete("/pages/{id}/delete")
async def delete_page(id: int, session: SessionDep):
    db = session
    await db.execute(delete(Page).where(Page.id == id))
    await db.commit()
    return RedirectResponse(url="/admin/pages", status_code=303)
