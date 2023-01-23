from typing import Optional, List
from uuid import uuid4, UUID

from fastapi import APIRouter, Request, Depends, Query
from opentracing import Format
from opentracing.ext import tags
from starlette import status
from starlette.responses import Response

from src.api.controller.order.dto.buy_order_input_dto import BuyOrderInputDto
from src.api.controller.order.dto.cancel_order_input_dto import CancelOrderInputDto
from src.api.controller.order.dto.get_order_output_dto import GetOrderOutputDto
from src.api.controller.order.dto.sell_order_input_dto import SellOrderInputDto
from src.api.controller.service_resolver import (
    get_order_service,
)
from src.api.handler.error_response import (
    generate_validation_error_response,
    ErrorResponse,
    generate_error_response,
)
from src.core.model.order.buy_order_input_model import BuyOrderInputModel
from src.core.model.order.cancel_order_input_model import CancelOrderInputModel
from src.core.model.order.get_order_output_model import GetOrderOutputModel
from src.core.model.order.sell_order_input_model import SellOrderInputModel
from src.infra.config.open_tracing_config import tracer

router = APIRouter()


@router.post(
    ":buy",
    response_model=None,
    status_code=status.HTTP_202_ACCEPTED,
    response_model_exclude_none=True,
    responses={
        status.HTTP_201_CREATED: {"model": None},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "content": generate_validation_error_response(
                invalid_field_location=["body", "user_id"]
            ),
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "content": generate_error_response(),
        },
    },
)
def buy_order(
    request: Request,
    buy_order_input_dto: BuyOrderInputDto,
    order_service=Depends(get_order_service),
):
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
    }
    with tracer.start_active_span(
        "OrderController-buy_order",
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        try:
            order_service.buy_order(
                buy_order_input_model=BuyOrderInputModel(**buy_order_input_dto.dict())
            )
            return Response(status_code=status.HTTP_202_ACCEPTED)
        finally:
            scope.close()


@router.post(
    ":sell",
    response_model=None,
    status_code=status.HTTP_202_ACCEPTED,
    response_model_exclude_none=True,
    responses={
        status.HTTP_201_CREATED: {"model": None},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "content": generate_validation_error_response(
                invalid_field_location=["body", "user_id"]
            ),
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "content": generate_error_response(),
        },
    },
)
def sell_order(
    request: Request,
    sell_order_input_dto: SellOrderInputDto,
    order_service=Depends(get_order_service),
):
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
    }
    with tracer.start_active_span(
        "OrderController-sell_order",
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        try:
            order_service.sell_order(
                sell_order_input_model=SellOrderInputModel(
                    **sell_order_input_dto.dict()
                )
            )
            return Response(status_code=status.HTTP_202_ACCEPTED)
        finally:
            scope.close()


@router.post(
    ":cancel",
    response_model=None,
    status_code=status.HTTP_202_ACCEPTED,
    response_model_exclude_none=True,
    responses={
        status.HTTP_201_CREATED: {"model": None},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "content": generate_validation_error_response(
                invalid_field_location=["body", "user_id"]
            ),
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "content": generate_error_response(),
        },
    },
)
def cancel_order(
    request: Request,
    cancel_order_input_dto: CancelOrderInputDto,
    order_service=Depends(get_order_service),
):
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
    }
    with tracer.start_active_span(
        "OrderController-cancel_order",
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        try:
            order_service.cancel_order(
                cancel_order_input_model=CancelOrderInputModel(
                    **cancel_order_input_dto.dict()
                )
            )
            return Response(status_code=status.HTTP_202_ACCEPTED)
        finally:
            scope.close()


@router.get(
    "",
    response_model=List[GetOrderOutputDto],
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    responses={
        status.HTTP_200_OK: {"model": List[GetOrderOutputDto]},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "content": generate_validation_error_response(
                invalid_field_location=["query", "user_id"]
            ),
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "content": generate_error_response(),
        },
    },
)
def get_orders(
    request: Request,
    user_id: Optional[UUID] = Query(None, example=uuid4()),
    order_service=Depends(get_order_service),
):
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
    }
    with tracer.start_active_span(
        "UserController-get_orders",
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        try:
            get_user_output_models: List[
                GetOrderOutputModel
            ] = order_service.get_orders(user_id=user_id)
            return [
                GetOrderOutputDto(**order_item.dict())
                for order_item in get_user_output_models
            ]
        finally:
            scope.close()


@router.get(
    "/{order_id}",
    response_model=GetOrderOutputDto,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    responses={
        status.HTTP_200_OK: {"model": GetOrderOutputDto},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "content": generate_validation_error_response(
                invalid_field_location=["query", "user_id"]
            ),
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "content": generate_error_response(),
        },
    },
)
def get_order(
    request: Request,
    order_id: UUID = Query(..., example=uuid4()),
    order_service=Depends(get_order_service),
):
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
    }
    with tracer.start_active_span(
        "UserController-get_order",
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        try:
            get_user_output_model: GetOrderOutputModel = order_service.get_order(
                order_id=order_id
            )
            return GetOrderOutputDto(**get_user_output_model.dict())

        finally:
            scope.close()
