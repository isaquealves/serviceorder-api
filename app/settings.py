import secrets

from decouple import Csv, config

DATABASES_CONFIG = {
    "default": "postgres",
    "postgres": {
        "driver": config("DB_DRIVER", "postgres"),
        "host": config("DB_HOST", "db"),
        "database": config("DB_NAME", "so"),
        "user": config("DB_USER", "so_user"),
        "password": config("DB_PASSWORD", "so_pass"),
        "port": 5432,
    },
    "testing": {
        "driver": config("TESTING_DB_DRIVER", "sqlite"),
        "database": config(
            "TESTING_DB", "/tmp/database-test.sqlite3"  # nosec
        ),
    },
}


class HardCoded:
    """Constants used throughout the application.

    All hard coded settings/data that are not actual/official
    configuration options for Flask or its extensions goes here.
    """

    ADMINS = config(
        "APP_ADMIN", cast=lambda v: [s.strip() for s in v.split(",")]
    )
    MAIL_EXCEPTION_THROTTLE = 24 * 60 * 60


class Development(HardCoded):
    """Default Flask configuration inherited by all environments."""

    DEBUG = config("DEBUG", True)
    TESTING = config("TESTING", False)
    SECRET_KEY = config(
        "SECRET_KEY", "1w0u1dcH0053423x1r3m311yL4rg3S1r12g1oB3U53DH3r3"
    )
    MAIL_SERVER = config("SMTP_SERVER", "smtp.localhost.test")
    MAIL_DEFAULT_SENDER = config("MAIL_SENDER", "admin@demo.test")
    MAIL_SUPPRESS_SEND = config("MAIL_SUPPRESS", True)
    REDIS_URL = config("REDIS_URL", "redis://localhost:6379/0")
    REDIS_CACHE_URL = config("REDIS_CACHE_URL", "redis://localhost:6379/2")
    ORATOR_DATABASES = DATABASES_CONFIG
    CELERY_BROKER_URL = config("CELERY_BROKER_URL", "redis://localhost:6379/1")
    CELERY_ACCEPT_CONTENT = config(
        "CELERY_ACCEPT_CONTENT", default="pickle", cast=Csv()
    )
    CELERY_RESULT_BACKEND = config(
        "CELERY_RESULT_BACKEND", "redis://localhost:6379/1"
    )
    CELERY_TASK_ALWAYS_EAGER = config(
        "CELERY_TASK_ALWAYS_EAGER", default="False", cast=bool
    )
    SENDGRID_API_KEY = config("SENDGRID_API_KEY", "NOAPIKEYHERE!OKBUDDY?")
    SENDGRID_DEFAULT_FROM = config(
        "SENDGRID_DEFAULT_FROM", "admin@example.com"
    )
    AUTH_CODE_VALID_UNTIL = config("AUTH_CODE_VALID_UNTIL", default=60)
    JWT_LIFETIME_SECONDS = config("JWT_LIFETIME_SECONDS", 3600)
    JWT_ALGORITHM = config("JWT_ALGORITHM", "HS256")
    JWT_SECRET = config("JWT_SECRET", secrets.token_urlsafe(128))


class Testing(Development):
    TESTING = True

    def __init__(self):
        self.ORATOR_DATABASES["default"] = "testing"
        self.CELERY_TASK_ALWAYS_EAGER = True
        self.AUTH_CODE_VALID_UNTIL = 30
        self.JWT_LIFETIME_SECONDS = config("JWT_LIFETIME_SECONDS", 1000)


class Production(Development):
    MAIL_SUPPRESS_SEND = False
    SECRET_KEY = config(
        "SECRET_KEY",
        "ud1d1pwAlEhF9RbbonJtSQQHzmbNMOmzEZ1NGULP09wgOI7dEkziTlFzp8VP2hYs",
    )
