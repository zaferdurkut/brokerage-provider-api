import logging

from src.infra.adapter.consumer.consumer_config import initialize_order_consumer_topic

logging.basicConfig(level=logging.INFO)


class NotificationConsumer:
    def __init__(self):
        logging.info("NotificationConsumer service was started")
        self.order_consumer = initialize_order_consumer_topic()

    def run(self):
        for msg in self.order_consumer:
            logging.info(msg)


NotificationConsumer().run()
