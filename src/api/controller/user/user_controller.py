from fastapi import APIRouter, Request, Depends
from fastapi import Header
from opentracing import Format
from opentracing.ext import tags
from pydantic import constr
from starlette import status
from starlette.responses import Response

from src.api.controller.service_resolver import (
    get_user_service,
)
from src.infra.config.open_tracing_config import tracer

router = APIRouter()


@router.post(
    "",
    response_model=None,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
def upsert(
    request: Request,
    user_service=Depends(get_user_service),
):
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
    }
    with tracer.start_active_span(
        "UserController-upsert",
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        try:
            return Response(status_code=status.HTTP_201_CREATED)
        finally:
            scope.close()
