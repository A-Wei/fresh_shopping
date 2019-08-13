import os
from dotenv import load_dotenv

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
    SECRET_KEY = os.environ("SECRET_KEY")

    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
    BASE_URL = "127.0.0.1:8000"
    CORS_ORIGIN_WHITELIST = ["http://localhost:3000"]


class Dev(Base):
    pass


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
