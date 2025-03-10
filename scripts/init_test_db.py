import asyncio

from db.database import SessionLocal, init_db
from db.models import Page


async def main():
    await init_db()
    sample_pages = [
        {"link": "https://example.com", "selector_type": "xpath", "selector": "//h1/text()", "comment": "Check title"},
        {
            "link": "https://python.org",
            "selector_type": "xpath",
            "selector": "/html/body/div/div[3]/div/section/div[2]/div[1]/div/ul/li[1]/a/text()",
            "comment": "Check official Python news",
        },
        {
            "link": "https://github.blog/",
            "selector_type": "xpath",
            "selector": "/html/body/main/div[1]/div/section/div/article[1]/h3/a/text()",
            "comment": "Check new articles from GitHub team blog",
        },
        {
            "link": "https://www.fontanka.ru/",
            "selector_type": "xpath",
            "selector": "/html/body/div[1]/div[1]/div[2]/main/div[5]/section[1]/div[2]/ol/li[1]/a/div/div/text()",
            "comment": "Fontanka news",
        },
        {
            "link": "https://lenta.ru/",
            "selector_type": "xpath",
            "selector": "/html/body/div[3]/div[3]/main/div[2]/section[1]/div[2]/div[2]/div[3]/a[1]/div[2]/h3/text()",
            "comment": "lenta news",
        },
    ]
    try:
        async with SessionLocal() as session:
            for page_data in sample_pages:
                page = Page(**page_data)
                session.add(page)
            await session.commit()
            print("Test DB initialized")
    except Exception as e:
        print(f"Error initializing test DB: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
