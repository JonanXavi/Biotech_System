import os
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    SECRET_KEY = 'my_secret_key'
    HOST=os.getenv("SERVER_HOST")
    PORT=os.getenv("DB_PORT")
    BD=os.getenv("DB_NAME")

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    CACHE_TYPE = "null"
    SEND_FILE_MAX_AGE_DEFAULT = 0

class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False