from importlib import import_module
import logging
import connexion
from app.providers.database import db

from app.models.user import User
from app.models.observers.user import UserObserver

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_config(config_class_string):
    config_module, config_class = config_class_string.rsplit('.', 1)
    config_class_object = getattr(import_module(config_module), config_class)

    return config_class_object()


def create_app(env, config=None):
    LOGGER.info('Starting app')
    connexion_app = connexion.FlaskApp(__name__, specification_dir="../docs/")
    connexion_app.add_api('service_order_api.yml',
                          options={"swagger_url": "/docs"})

    app = connexion_app.app
    if config:
        config_dict = dict([(k, getattr(config, k))
                            for k in dir(config) if not k.startswith('_')])
    app.config.update(config_dict)
    db.init_app(app)

    User.observe(UserObserver())

    return app
