from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from db.models import Log, News, Page
from models.interface import DeletePageResponse
from models.observer import Observer
from models.structures import Log as LogSchema
from models.structures import News as NewsSchema
from models.structures import Page as PageSchema
from models.structures import PageBase

from .dependecies import SessionDep

router = APIRouter(
    prefix="",
    tags=["Pages"],
)


async def check_page_exists(id: int, session: SessionDep) -> None:
    db = session
    page = await db.execute(select(Page).filter(Page.id == id))
    page = page.scalars().first()
    return bool(page)


async def validate_page_exists(
    id: int,
    session: SessionDep,
) -> None:
    if not await check_page_exists(id, session):
        raise HTTPException(status_code=404, detail="Page not found")
    return id


@router.get("/pages", response_model=list[PageSchema], summary="Get all observed pages")
async def get_all_pages(session: SessionDep) -> list[Page]:
    db = session
    pages = await db.execute(select(Page))
    pages = pages.scalars().all()
    return pages


@router.get("/pages/{id}", response_model=PageSchema, summary="Get page by id")
async def get_page_by_id(session: SessionDep, id: int = Depends(validate_page_exists)) -> Page:
    db = session
    page = await db.execute(select(Page).filter(Page.id == id))
    page = page.scalars().first()
    return page


@router.post("/pages", response_model=PageSchema, summary="Create new page")
async def create_page(request: PageBase, session: SessionDep) -> Page:
    db = session
    page = Page(**request.model_dump())
    db.add(page)
    await db.commit()
    await db.refresh(page)
    return page


@router.put("/pages/{id}", response_model=PageSchema, summary="Update page by id")
async def update_page(request: PageBase, session: SessionDep, id: int = Depends(validate_page_exists)) -> Page:
    db = session
    page = await db.execute(select(Page).filter(Page.id == id))
    page = page.scalars().first()
    for key, value in request.model_dump().items():
        setattr(page, key, value)
    await db.commit()
    await db.refresh(page)
    return page


@router.delete("/pages/{id}", summary="Delete page by id", response_model=DeletePageResponse)
async def delete_page(session: SessionDep, id: int = Depends(validate_page_exists)) -> DeletePageResponse:
    db = session
    page = await db.execute(select(Page).filter(Page.id == id))
    page = page.scalars().first()
    db.delete(page)
    await db.commit()
    return {"message": "Page deleted", "page": page}


@router.get("/pages/{id}/logs", summary="Get logs by page id", response_model=list[LogSchema])
async def get_logs_by_page_id(session: SessionDep, id: int = Depends(validate_page_exists)) -> list[LogSchema]:
    db = session
    logs = await db.execute(select(Log).filter(Log.page_id == id))
    logs = logs.scalars().all()
    return logs


@router.get("/news", summary="Get all news", response_model=list[NewsSchema])
async def get_news(session: SessionDep) -> list[NewsSchema]:
    db = session
    news = await db.execute(select(News))
    news = news.scalars().all()
    return news


@router.post("/check_changes", summary="Check changes in pages")
async def check_changes(session: SessionDep) -> None:
    db = session
    await Observer.check_changes(db)
