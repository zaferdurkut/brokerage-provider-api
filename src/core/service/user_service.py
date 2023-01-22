from uuid import UUID

from opentracing_instrumentation import get_current_span

from src.core.model.user.create_user_input_model import CreateUserInputModel
from src.core.model.user.create_user_output_model import CreateUserOutputModel
from src.core.model.user.get_user_output_model import GetUserOutputModel
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
            return self.user_repository_port.create_user(
                create_user_input_model=create_user_input_model
            )

    def get_user(self, user_id: UUID) -> GetUserOutputModel:
        with tracer.start_active_span(
            "UserService-get_user",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "user_id",
                user_id,
            )
            return self.user_repository_port.get_user(user_id=user_id)
