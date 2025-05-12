import logging
from contextlib import asynccontextmanager

from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.logging import configure_logging
from app.routers import admin_router, router
from models.observer import Observer

observer = Observer()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    try:
        observer.scheduler.add_job(
            func=observer.scheduled_check_changes, trigger=IntervalTrigger(minutes=1), id="check_changes"
        )
        observer.scheduler.start()
        yield
    except Exception as e:
        logger.error(f"Scheduler error: {e}")
        raise
    observer.scheduler.shutdown()
    logger.info("Scheduler stopped")


app = FastAPI(lifespan=lifespan)

app.include_router(router)
app.include_router(admin_router)


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")


@app.get("/admin", include_in_schema=False)
async def admin_redirect():
    return RedirectResponse(url="/admin/pages")
