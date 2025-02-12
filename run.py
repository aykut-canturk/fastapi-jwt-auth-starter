import uuid
from fastapi.responses import JSONResponse
from fastapi import Request
from jwt import ExpiredSignatureError
from app.config import jwt_settings
from app import create_app
from app.utils.logger import (
    get_correlation_id,
    set_correlation_id,
    log_exception,
    log_info,
    log_debug,
)
from app.models.database import create_db_and_tables
from app.routes import initialize_routes
from app.utils.starter import insert_root_user
from app.utils.exception import ValidationError
from app.security import set_current_user_id

app = create_app()


async def log_request(request: Request, level="info"):
    request_log = {
        "path": request.url.path,
        "method": request.method,
        "query_params": request.query_params,
        "headers": request.headers,
    }
    try:
        request_log["body"] = await request.json()
    except Exception:
        request_log["body"] = "Unable to read body"

    if level == "debug":
        log_debug(f"Request: {request_log}")
    else:
        log_info(f"Request: {request_log}")


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    log_exception(exc)
    await log_request(request)

    return JSONResponse(
        status_code=400,
        content={"message": exc.message, "code": get_correlation_id()},
    )


@app.exception_handler(ExpiredSignatureError)
async def expired_signature_error_handler(request: Request, exc: ExpiredSignatureError):
    return JSONResponse(
        status_code=400,
        content={"message": "Token has expired."},
    )


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    log_exception(exc)
    await log_request(request)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error."},
    )


@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    set_correlation_id(correlation_id)
    await log_request(request, level="debug")
    response = await call_next(request)
    log_debug(f"Response status: {response.status_code}")
    response.headers["X-Correlation-ID"] = correlation_id
    return response


@app.middleware("http")
async def current_user_id_middleware(request: Request, call_next):
    if "Authorization" in request.headers:
        parts = request.headers["Authorization"].split(" ")
        if len(parts) == 2 and parts[0].lower() == "bearer":
            token = parts[1]
            if token:
                await set_current_user_id(token)
    return await call_next(request)


app.get("/")(lambda: {"message": "Hello, World!"})

initialize_routes(app)
create_db_and_tables()
insert_root_user()
