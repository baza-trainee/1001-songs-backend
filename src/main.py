import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from sqladmin import Admin

from src.config import (
    ALLOW_HEADERS,
    ALLOW_METHODS,
    ORIGINS,
    PROJECT_NAME,
    SWAGGER_PARAMETERS,
    API_PREFIX,
)
from src.admin import __all__ as views
from src.utils import lifespan
from src.database.database import engine, async_session_maker
from src.admin.auth import authentication_backend
from src.auth.routers import auth_router
from src.payment.routers import payment_router
from src.footer.routers import footer_router
from src.our_team.routers import team_router
from src.education.routers import education_router
from src.about.routers import about_router
from src.location.routers import location_router, map_router
from src.news.routers import news_router


app = FastAPI(
    swagger_ui_parameters=SWAGGER_PARAMETERS,
    title=PROJECT_NAME,
    lifespan=lifespan,
)

admin = Admin(
    app,
    engine,
    authentication_backend=authentication_backend,
    title="1001-ADMIN",
    session_maker=async_session_maker,
)

app.mount("/static", StaticFiles(directory="static"), name="static")
api_routers = [
    auth_router,
    payment_router,
    footer_router,
    team_router,
    education_router,
    about_router,
    location_router,
    news_router,
    map_router,
]

[app.include_router(router, prefix=API_PREFIX) for router in api_routers]

[admin.add_view(view) for view in views]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADERS,
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time"] = f"{round(process_time)} ms"
    return response


add_pagination(app)
