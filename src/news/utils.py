from sqlalchemy.ext.asyncio import AsyncSession

from .models import NewsCategory, News
from .exceptions import AFTER_NEWS_CATEGORY_CREATE, AFTER_NEWS_CREATE


async def create_news_category(news_list: list[dict], session: AsyncSession):
    try:
        add_data = []
        for news in news_list:
            instance = NewsCategory(**news)
            add_data.append(instance)
        session.add_all(add_data)
        print(AFTER_NEWS_CATEGORY_CREATE)
    except Exception as exc:
        raise exc


async def create_news(news_list: list[dict], session: AsyncSession):
    try:
        add_data = []
        for region in news_list:
            instance = News(**region)
            add_data.append(instance)
        session.add_all(add_data)
        print(AFTER_NEWS_CREATE)
    except Exception as exc:
        raise exc
