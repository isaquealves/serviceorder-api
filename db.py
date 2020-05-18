import sys

# from docopt import docopt
from app import create_app, get_config
from app.providers.database import db

# OPTIONS = docopt(__doc__) if __name__ == '__main__' else dict()
SETTINGS_CLASS_STRING = {
    "prod": "app.settings.Production",
    "dev": "app.settings.Development",
    "testing": "app.settings.Testing",
}


if __name__ == "__main__":
    env = sys.argv.pop(1)
    settings = get_config(SETTINGS_CLASS_STRING[env])
    app = create_app(settings)
    db.init_app(app)
    db.cli.run()
