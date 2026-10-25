
import logging

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


async def http_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    if isinstance(exc, StarletteHTTPException):
        message = (
            exc.detail
            if isinstance(exc.detail, str)
            else "Request failed"
        )
        status_code = exc.status_code
        headers = exc.headers
    else:
        message = "Request failed"
        status_code = 500
        headers = None

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": None,
        },
        headers=headers,
    )


async def validation_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    errors = (
        jsonable_encoder(exc.errors())
        if isinstance(exc, RequestValidationError)
        else []
    )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Request validation failed",
            "data": {"errors": errors},
        },
    )


async def database_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.error("Database operation failed", exc_info=exc)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "A database error occurred",
            "data": None,
        },
    )


async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.error("Unexpected application error", exc_info=exc)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "An unexpected error occurred",
            "data": None,
        },
    )
