from fastapi import FastAPI

from ${project["fixed_project_name"]}.routers import router


def build_app(app: FastAPI, /) -> None:
    app.include_router(router)
