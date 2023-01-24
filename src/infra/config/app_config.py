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
REDIS_USER_DB = config("REDIS_USER_DB", int)

# Kafka
KAFKA_ORDER_TOPIC = config("KAFKA_ORDER_TOPIC")
KAFKA_NOTIFICATION_TOPIC = config("KAFKA_NOTIFICATION_TOPIC")
KAFKA_CONSUMER_SERVERS = config("KAFKA_CONSUMER_SERVERS")
KAFKA_PRODUCER_SERVERS = config("KAFKA_PRODUCER_SERVERS")

# Telegram Notification
NOTIFICATION_TELEGRAM_BOT_TOKEN = config("NOTIFICATION_TELEGRAM_BOT_TOKEN")
NOTIFICATION_TELEGRAM_CHAT_ID = config("NOTIFICATION_TELEGRAM_CHAT_ID")
