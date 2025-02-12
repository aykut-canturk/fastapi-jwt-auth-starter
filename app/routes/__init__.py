from fastapi import FastAPI, Depends
from app.routes.auth import router as auth_router
from app.routes.user import router as user_router
from app.security import verify_access_token


def _add_secure_router(app: FastAPI, router, prefix: str, tags: list):
    app.include_router(
        router,
        prefix=prefix,
        tags=tags,
        dependencies=[Depends(verify_access_token)],
    )


def initialize_routes(app: FastAPI):
    app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
    _add_secure_router(app, user_router, prefix="/api/users", tags=["users"])
