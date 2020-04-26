from decouple import config

DATABASES_CONFIG = {
        'default': 'postgres',
        'postgres': {
            'driver': config('DB_DRIVER', 'postgres'),
            'host': config('DB_HOST', 'localhost'),
            'database': config('DB_NAME', 'so'),
            'user': config('DB_USER', 'so_user'),
            'password': config('DB_PASSWORD', 'so_pass'),
            'port': 5432
        },
        'testing': {
            'driver': config('TESTING_DB_DRIVER', 'sqlite'),
            'database': config('TESTING_DB', '/tmp/database-test.sqlite3')
        }
    }


class HardCoded:
    """Constants used throughout the application.

    All hard coded settings/data that are not actual/official
    configuration options for Flask or its extensions goes here.
    """
    ADMINS = config(
        'APP_ADMIN', 
        cast=lambda v: [s.strip() for s in v.split(',')]
    )
    MAIL_EXCEPTION_THROTTLE = 24 * 60 * 60


class Development(HardCoded):
    """Default Flask configuration inherited by all environments."""
    DEBUG = config('DEBUG', True)
    TESTING = config('TESTING', False)
    SECRET_KEY = config(
        'SECRET_KEY', 
        '1w0u1dcH0053423x1r3m311yL4rg3S1r12g1oB3U53DH3r3'
    )
    MAIL_SERVER = config('SMTP_SERVER', 'smtp.localhost.test')
    MAIL_DEFAULT_SENDER = config('MAIL_SENDER', 'admin@demo.test')
    MAIL_SUPPRESS_SEND = config('MAIL_SUPPRESS', True)
    REDIS_URL = config('REDIS_URL', 'redis://localhost/0')
    ORATOR_DATABASES = DATABASES_CONFIG


class Testing(Development):
    TESTING = True

    def __init__(self):
        self.ORATOR_DATABASES['default'] = 'testing'


class Production(Development):
    MAIL_SUPPRESS_SEND = False
    SECRET_KEY = config(
        'SECRET_KEY',
        'ud1d1pwAlEhF9RbbonJtSQQHzmbNMOmzEZ1NGULP09wgOI7dEkziTlFzp8VP2hYs'
    )

