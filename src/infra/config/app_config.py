from dotenv import load_dotenv
from starlette.config import Config

load_dotenv()

config = Config(".env")

JAEGER_HOST = config("JAEGER_HOST")
JAEGER_PORT = config("JAEGER_PORT")
JAEGER_SAMPLER_TYPE = config("JAEGER_SAMPLER_TYPE")
JAEGER_SAMPLER_RATE = config("JAEGER_SAMPLER_RATE")

DATABASE_URL = config("DATABASE_URL")

# Redis
REDIS_HOST = config("REDIS_HOST")
REDIS_PORT = config("REDIS_PORT")
REDIS_DB = config("REDIS_DB")

# Kafka
KAFKA_ORDER_TOPIC = config("KAFKA_ORDER_TOPIC")
KAFKA_NOTIFICATION_TOPIC = config("KAFKA_NOTIFICATION_TOPIC")
KAFKA_CONSUMER_GROUP = config("KAFKA_CONSUMER_GROUP")
KAFKA_SERVERS = config("KAFKA_SERVERS")
