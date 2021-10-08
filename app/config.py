import os

class Config(object):
    SECRET_KEY = 'my_secret_key'

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    CACHE_TYPE = "null"
    SEND_FILE_MAX_AGE_DEFAULT = 0

class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False