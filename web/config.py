import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = False
    SESSION_TYPE = 'mongodb'
    SERVER_NAME = os.getenv('SERVER_NAME')
    BASE_URL = os.getenv('BASE_URL')
    SESSION_COOKIE_SECURE = (os.getenv('SESSION_COOKIE_SECURE') == 'true')
    PERMANENT_SESSION_LIFETIME = int(os.getenv('PERMANENT_SESSION_LIFETIME'))
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI')
    CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
    CONSUMER_KEY = os.getenv('CONSUMER_KEY')
    REDIS_HOSTNAME = os.getenv('REDIS_HOSTNAME')
    REDIS_PORT = int(os.getenv('REDIS_PORT'))
    REDIS_PUBSUB_CH = os.getenv('REDIS_PUBSUB_CH')