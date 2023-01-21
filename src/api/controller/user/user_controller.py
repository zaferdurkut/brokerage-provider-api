from fastapi import APIRouter, Request, Depends
from opentracing import Format
from opentracing.ext import tags
from starlette import status

from src.api.controller.service_resolver import (
    get_user_service,
)
from src.api.controller.user.dto.create_user_input_dto import CreateUserInputDto
from src.api.controller.user.dto.create_user_output_dto import CreateUserOutputDto
from src.api.handler.error_response import (
    ErrorResponse,
    generate_validation_error_response,
    generate_error_response,
)
from src.core.model.user.create_user_input_model import CreateUserInputModel
from src.infra.config.open_tracing_config import tracer

router = APIRouter()


@router.post(
    "",
    response_model=CreateUserOutputDto,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
    responses={
        status.HTTP_201_CREATED: {"model": CreateUserOutputDto},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "content": generate_validation_error_response(
                invalid_field_location=["body", "name"]
            ),
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "content": generate_error_response(),
        },
    },
)
def create_user(
    request: Request,
    user_input_dto: CreateUserInputDto,
    user_service=Depends(get_user_service),
):
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
    }
    with tracer.start_active_span(
        "UserController-create_user",
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        try:
            create_user_output_model: CreateUserInputModel = user_service.create_user(
                create_user_input_model=CreateUserInputModel(**user_input_dto.dict())
            )
            return CreateUserOutputDto(**create_user_output_model.dict())
        finally:
            scope.close()
