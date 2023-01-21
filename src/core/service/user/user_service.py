from typing import Any

from opentracing_instrumentation import get_current_span

from src.core.port.user_repository_port import UserRepositoryPort
from src.infra.config.open_tracing_config import tracer


class UserService:
    def __init__(
        self,
        user_repository_port: UserRepositoryPort,
    ):
        self.user_repository_port = user_repository_port

    def create_user(self, user_input_model: Any = None):
        with tracer.start_active_span(
            "UserService-create_user",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "user_input_model",
                user_input_model,
            )
