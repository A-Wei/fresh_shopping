import os
from dotenv import load_dotenv

load_dotenv()
class Base:
    DEBUG = True
    HEROKU = os.getenv("HEROKU")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres",
            "USER": "postgres",
            # "HOST": "db",  # set in docker-compose.yml
            "HOST": "localhost",
            "PORT": 5432,
        }
    }
    SECRET_KEY = os.getenv("SECRET_KEY")
    MESSAGE_BROKER = os.environ["MESSAGE_BROKER"]

    EMAIL_HOST = os.environ["EMAIL_HOST"]
    EMAIL_PORT = os.environ["EMAIL_PORT"]
    EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
    EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]

    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

    BASE_URL = "127.0.0.1:8000"
    CORS_ORIGIN_WHITELIST = ["http://localhost:3000"]

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }


class Dev(Base):
    EMAIL_HOST = "127.0.0.1"
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
    EMAIL_PORT = 1025
    EMAIL_USE_TLS = False



class Test(Base):
    DEBUG = False
    if Base.HEROKU:
        DATABASES = {}
    else:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "travis_test",
                "USER": "travis",
                "HOST": "localhost",  # set in docker-compose.yml
                "PORT": 5432,  # default postgres port
            }
        }


class Staging(Base):
    DEBUG = False


class Prod(Base):
    DEBUG = False
    DATABASES = {}


def get_config():
    env = os.environ["ENV"]

    if env == "production":
        return Prod()

    if env == "test":
        return Test()

    if env == "staging":
        return Staging()

    return Dev()
