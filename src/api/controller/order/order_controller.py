from fastapi import APIRouter, Request, Depends
from opentracing import Format
from opentracing.ext import tags
from starlette import status
from starlette.responses import Response

from src.api.controller.service_resolver import (
    get_order_service,
)
from src.api.controller.order.dto.order_event_input_dto import CreateOrderInputDto
from src.api.handler.error_response import (
    generate_validation_error_response,
    ErrorResponse,
    generate_error_response,
)
from src.core.model.order.order_event_input_model import CreateOrderInputModel
from src.infra.config.open_tracing_config import tracer

router = APIRouter()


@router.post(
    "",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
    responses={
        status.HTTP_201_CREATED: {"model": None},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "content": generate_validation_error_response(
                invalid_field_location=["page", "page_size"]
            ),
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "content": generate_error_response(),
        },
    },
)
def create_order(
    request: Request,
    order_input_dto: CreateOrderInputDto,
    order_service=Depends(get_order_service),
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
            order_service.create_order(
                order_event_input_model=CreateOrderInputModel(**order_input_dto.dict())
            )
            return Response(status_code=status.HTTP_201_CREATED)
        finally:
            scope.close()
