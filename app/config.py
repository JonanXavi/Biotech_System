import os

'''BDD'''
username = ''
password = ''
dsn = '192.168.100.136/xe'
port = 1521
encoding = 'UTF-8'

class Config(object):
    SECRET_KEY = 'my_secret_key'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass