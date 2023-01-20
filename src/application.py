from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from src.api.controller.health_check import health_check_controller
from src.api.controller.user import user_controller
from src.api.handler.exception_handler import (
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
    not_found_exception_handler,
    infra_exception_handler,
    bad_request_exception_handler,
)
from src.api.middleware.request_response_middleware import RequestResponseMiddleware
from src.infra.exception.bad_request_exception import BadRequestException
from src.infra.exception.infra_exception import InfraException
from src.infra.exception.not_found_exception import NotFoundException


def create_app():
    app = FastAPI(
        title="Stock Exchange API",
        description="The API for the stock exchange operations",
        version="0.1.0",
        openapi_url="/openapi.json",
        docs_url="/",
        redoc_url="/redoc",
    )

    app.add_exception_handler(Exception, unhandled_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(InfraException, infra_exception_handler)
    app.add_exception_handler(BadRequestException, bad_request_exception_handler)
    app.add_middleware(RequestResponseMiddleware)

    app.include_router(
        health_check_controller.router, prefix="/api", tags=["health check"]
    )

    app.include_router(
        user_controller.router,
        prefix="/api/v1/users",
        tags=["user"],
    )

    return app
