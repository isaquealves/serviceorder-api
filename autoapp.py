import logging
from decouple import config

from app import create_app, get_config

settings_class_string = {
    "prod": "app.settings.Production",
    "dev": "app.settings.Development",
    "testing": "app.settings.Testing",
}

logging.basicConfig(level=logging.DEBUG)


handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter(logging.DEBUG))


env = config("FLASK_ENV", default="dev")
settings = get_config(settings_class_string[env])
app = create_app(config=settings)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)
