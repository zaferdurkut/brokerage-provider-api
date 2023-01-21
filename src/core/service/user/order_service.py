import uuid

from opentracing_instrumentation import get_current_span

from src.core.model.order.create_order_output_model import CreateOrderOutputModel
from src.core.model.order.order_event_input_model import CreateOrderInputModel
from src.core.port.order_event_publish_port import OrderEventPublishPort
from src.infra.config.open_tracing_config import tracer


class OrderService:
    def __init__(
        self,
        order_event_publish_port: OrderEventPublishPort,
    ):
        self.order_event_publish_port = order_event_publish_port

    def create_order(
        self, order_event_input_model: CreateOrderInputModel
    ) -> CreateOrderOutputModel:
        with tracer.start_active_span(
            "UserService-create_user",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "order_event_input_model",
                order_event_input_model,
            )
            self.order_event_publish_port.create_order_event(
                order_event_input_model=order_event_input_model
            )
            return CreateOrderOutputModel(id=uuid.uuid4())
