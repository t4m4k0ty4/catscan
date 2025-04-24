import logging
import re

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from lxml import html
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import SessionLocal
from db.models import Log, News, Page

logger = logging.getLogger(__name__)


class Observer:
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()

    @staticmethod
    async def get_current_value(page: Page) -> tuple[bool, str | None]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(page.link)
                response.raise_for_status()
                http_content = response.text
                value = None
                if page.selector_type == "xpath":
                    tree = html.fromstring(http_content)
                    elements = tree.xpath(page.selector)
                    if page.selector.endswith("/text()"):
                        value = elements[0]
                    else:
                        value = elements[0].text_content().strip() if elements else None
                elif page.selector_type == "regex":
                    match = re.search(page.selector, http_content)
                    value = match.group(0) if match else None
                value = value.replace("\n", "").replace("\t", "") if value else None
                return True, value
        except Exception as e:
            return False, str(e)

    @staticmethod
    async def check_changes(session: AsyncSession) -> None:
        logger.info("Starting change check...")
        pages = await session.execute(select(Page))
        pages = pages.scalars().all()
        for page in pages:
            last_log = await session.execute(select(Log).filter(Log.page_id == page.id).order_by(Log.created_at.desc()))
            last_log = last_log.scalars().first()
            prev_value = last_log.current_value if last_log else None
            success, result = await Observer.get_current_value(page)
            if success:
                current_value = result
                error_message = None
                if current_value == prev_value:
                    continue
                logger.info(
                    f"Change detected on page {page.link}: old value '{prev_value or 'None'}', new value '{current_value or 'None'}'"
                )
                title = f"Changes detected in {page.link}"
                description = f"Previous value: {prev_value}\nCurrent value: {current_value}"
                new_news = News(page_id=page.id, title=title, description=description)
                session.add(new_news)
                logger.info(f"New news entry created for page {page.link}")
            else:
                current_value = None
                error_message = result
                logger.error(f"Error while checking changes on page {page.link}: {error_message}")
            new_log = Log(
                page_id=page.id, prev_value=prev_value, current_value=current_value, error_message=error_message
            )
            session.add(new_log)
        await session.commit()
        logger.info("Change check completed.")

    async def scheduled_check_changes(self) -> None:
        async with SessionLocal() as session:
            await self.check_changes(session)


if __name__ == "__main__":
    ...
