import requests

from src.infra.config.app_config import NOTIFICATION_TELEGRAM_BOT_TOKEN

url = f"https://api.telegram.org/bot{NOTIFICATION_TELEGRAM_BOT_TOKEN}/getUpdates"


if __name__ == "__main__":
    print(requests.get(url).json())
