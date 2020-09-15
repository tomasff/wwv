import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    DB_HOSTNAME = os.getenv('DB_HOSTNAME')
    DB_PORT = int(os.getenv('DB_PORT'))
    DB_NAME = os.getenv('DB_NAME')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    BASE_URL = os.getenv('BASE_URL')
    REDIS_HOSTNAME = os.getenv('REDIS_HOSTNAME')
    REDIS_PORT = int(os.getenv('REDIS_PORT'))
    REDIS_PUBSUB_CH = os.getenv('REDIS_PUBSUB_CH')