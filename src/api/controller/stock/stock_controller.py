from fastapi import APIRouter, Request, Depends
from opentracing import Format
from opentracing.ext import tags
from starlette import status
from starlette.responses import Response

from src.api.controller.service_resolver import (
    get_stock_service,
)
from src.api.controller.stock.dto.create_stock_input_dto import CreateStockInputDto
from src.api.handler.error_response import (
    generate_validation_error_response,
    ErrorResponse,
    generate_error_response,
)
from src.core.model.stock.create_stock_input_model import CreateStockInputModel
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
                invalid_field_location=["body", "amount"]
            ),
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "content": generate_error_response(),
        },
    },
)
def create_stock(
    request: Request,
    stock_input_dto: CreateStockInputDto,
    stock_service=Depends(get_stock_service),
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
            stock_service.create_stock(
                create_stock_input_model=CreateStockInputModel(**stock_input_dto.dict())
            )
            return Response(status_code=status.HTTP_201_CREATED)
        finally:
            scope.close()
