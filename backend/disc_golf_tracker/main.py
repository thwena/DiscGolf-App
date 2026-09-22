from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .auth import router as auth_router
from .config import Settings
from .database import Database


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved_settings = settings or Settings.from_env()
    database = Database(resolved_settings.database_path)

    @asynccontextmanager
    async def lifespan(application: FastAPI):
        database.migrate()
        application.state.database = database
        application.state.settings = resolved_settings
        yield

    application = FastAPI(
        title="Disc Golf Tracker API",
        version="0.1.0-dev",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )
    application.add_middleware(
        TrustedHostMiddleware, allowed_hosts=list(resolved_settings.trusted_hosts)
    )
    application.include_router(auth_router)

    @application.get("/api/health/live", tags=["health"])
    def live() -> dict[str, str]:
        return {"status": "ok"}

    @application.get("/api/health/ready", tags=["health"])
    def ready() -> dict[str, str]:
        if not database.ready():
            raise HTTPException(status_code=503, detail="Database is unavailable")
        return {"status": "ready"}

    static_dir = resolved_settings.static_dir
    assets_dir = static_dir / "assets"
    if assets_dir.is_dir():
        application.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @application.get("/{path:path}", include_in_schema=False)
    def frontend(request: Request, path: str) -> FileResponse:
        requested = (static_dir / path).resolve()
        if path and requested.is_relative_to(static_dir) and requested.is_file():
            return FileResponse(requested)
        index = static_dir / "index.html"
        if index.is_file():
            return FileResponse(index)
        raise HTTPException(status_code=404, detail="Frontend has not been built")

    return application
