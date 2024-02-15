from sqlalchemy.ext.asyncio import AsyncSession

from .models import OurProject
from .exceptions import AFTER_PROJECTS_CREATE


async def create_projects(project_list: list[dict], session: AsyncSession):
    from src.utils import write_filetype_field

    try:
        field = "preview_photo"
        add_data = []
        for project in project_list:
            if project[field]:
                project[field] = await write_filetype_field(project[field])
            instance = OurProject(**project)
            add_data.append(instance)
        session.add_all(add_data)
        print(AFTER_PROJECTS_CREATE)
    except Exception as exc:
        raise exc
