from httpx import AsyncClient
import pytest

from src.database.redis import invalidate_cache
from scripts.fake_data import FAKE_TEAM
from scripts.initial_db import add_instances
from src.our_team.models import OurTeam
from tests.conftest import get_session_context


@pytest.fixture(autouse=True, scope="session")
async def team_data():
    data = map(lambda self: self.copy(), FAKE_TEAM)
    async with get_session_context() as s:
        add_instances(model=OurTeam, data=data, session=s)
        await s.commit()


async def test_get_list_team(ac: AsyncClient):
    response = await ac.get("/api/v1/team")
    assert response.status_code == 200

    team_list = response.json()
    for number, partipant in enumerate(team_list):
        assert partipant["full_name"] == FAKE_TEAM[number]["full_name"]
        assert partipant["description"] == FAKE_TEAM[number]["description"]
        assert partipant["photo"].endswith(".png")


async def test_list_team_cache(ac: AsyncClient):
    for _ in range(2):
        response = await ac.get("/api/v1/team")
    etag = response.headers.get("etag", None)
    assert etag

    match_header = {"If-None-Match": etag}
    response = await ac.get("/api/v1/team", headers=match_header)
    assert response.status_code == 304

    await invalidate_cache("get_team_list")
    response = await ac.get("/api/v1/team", headers=match_header)
    assert response.status_code == 200
