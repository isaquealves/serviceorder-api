import logging
import connexion
from connexion.resolver import RestyResolver

from app.providers.database import db

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def create_app(env, additional_settings=None):
    LOGGER.info('Starting app')
    connexion_app = connexion.FlaskApp(__name__, specification_dir="../docs/")
    connexion_app.add_api('service_order_api.yml', options={"swagger_url": "/docs"})

    app = connexion_app.app
    app.config.update(additional_settings)
    db.init_app(app)

    return app
    

    
