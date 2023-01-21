from src.infra.adapter.consumer.kafka.consumer_config import initialize_order_consumer
from src.infra.config.logging_config import get_logger

logger = get_logger()


class OrderConsumer:
    def __init__(self):
        self.order_consumer = initialize_order_consumer()

    def run(self):
        logger.warning("OrderConsumer service was started")
        for message in self.order_consumer:
            print(message)


OrderConsumer().run()
