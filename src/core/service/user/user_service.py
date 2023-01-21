from typing import Any
from uuid import uuid4

from opentracing_instrumentation import get_current_span

from src.core.model.user.create_user_input_model import CreateUserInputModel
from src.core.model.user.create_user_output_model import CreateUserOutputModel
from src.core.port.user_repository_port import UserRepositoryPort
from src.infra.config.open_tracing_config import tracer


class UserService:
    def __init__(
        self,
        user_repository_port: UserRepositoryPort,
    ):
        self.user_repository_port = user_repository_port

    def create_user(
        self, create_user_input_model: CreateUserInputModel
    ) -> CreateUserOutputModel:
        with tracer.start_active_span(
            "UserService-create_user",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "create_user_input_model",
                create_user_input_model,
            )
            return CreateUserOutputModel(id=uuid4())
