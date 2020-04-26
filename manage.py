"""Main entry-point into the 'PyPI Portal' Flask and Celery application.

This is a demo Flask application used to show how I structure my large Flask
applications.

License: MIT
Website: https://github.com/Robpol86/Flask-Large-Application-Example

Command details:
    shell               Starts a Python interactive shell with the Flask
                        application context.

Usage:

    manage.py shell [--env=ENV]
    manage.py (-h | --help)

Options:
    --env=ENV                   Load the configuration based on environment.
    -l DIR --log_dir=DIR        Log all statements to file in this directory
                                instead of stdout.
                                Only ERROR statements will go to stdout. stderr
                                is not used.
    -n NUM --name=NUM           Celery Worker name integer.
                                [default: 1]
    --pid=FILE                  Celery Beat PID file.
                                [default: ./celery_beat.pid]
    -p NUM --port=NUM           Flask will listen on this port number.
                                [default: 5000]
    -s FILE --schedule=FILE     Celery Beat schedule database file.
                                [default: ./celery_beat.db]
"""
from __future__ import print_function
from functools import wraps
import logging
import logging.handlers
import os
import signal
import sys

from docopt import docopt
import flask
from flask_script import Shell

from app import create_app, get_config
from app.providers.database import db

OPTIONS = docopt(__doc__) if __name__ == '__main__' else dict()


class CustomFormatter(logging.Formatter):
    LEVEL_MAP = {logging.FATAL: 'F', logging.ERROR: 'E',
                 logging.WARN: 'W', logging.INFO: 'I', logging.DEBUG: 'D'}

    def format(self, record):
        record.levelletter = self.LEVEL_MAP[record.levelno]
        return super(CustomFormatter, self).format(record)


def parse_options():
    """Parses command line options for Flask.

    Returns:
    Config instance to pass into create_app().
    """
    settings_class_string = {
        'prod': 'app.settings.Production',
        'dev': 'app.settings.Development',
        'testing': 'app.settings.Testing'
    }
    # Figure out which class will be imported.
    config_class_string = settings_class_string['dev']
    if OPTIONS['--env']:
        config_class_string = settings_class_string[OPTIONS['--env']]

    config_obj = get_config(config_class_string)

    return config_obj


def setup_logging(name=None):
    """Setup Google-Style logging for the entire application.

    See: https://bit.ly/3bFjLXd

    Always logs DEBUG statements somewhere.

    Positional arguments:
    name -- Append this string to the log file filename.
    """
    log_to_disk = False
    if OPTIONS['--log_dir']:
        if not os.path.isdir(OPTIONS['--log_dir']):
            print('ERROR: Directory {} does not exist.'.format(
                OPTIONS['--log_dir']))
            sys.exit(1)
        if not os.access(OPTIONS['--log_dir'], os.W_OK):
            print('ERROR: No permissions to write to directory {}.'.format(
                OPTIONS['--log_dir']))
            sys.exit(1)
        log_to_disk = True
    
    fmt = '%(levelletter)s%(asctime)s.%(msecs).03d %(process)d %(filename)s:%(lineno)d] %(message)s'  # noqa: E501
    datefmt = '%m%d %H:%M:%S'
    formatter = CustomFormatter(fmt, datefmt)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.ERROR if log_to_disk else logging.DEBUG)
    console_handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(console_handler)

    if log_to_disk:
        file_name = os.path.join(
            OPTIONS['--log_dir'], 'pypi_portal_{}.log'.format(name))
        file_handler = logging.handlers.TimedRotatingFileHandler(
            file_name, when='d', backupCount=7)
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)


def command(func):
    """Decorator that registers the chosen command/function.

    If a function is decorated with @command but that function name is not a valid "command" according to the docstring,  # noqa: E501
    a KeyError will be raised, since that's a bug in this script.

    If a user doesn't specify a valid command in their command line arguments, the above docopt(__doc__) line will print  # noqa: E501
    a short summary and call sys.exit() and stop up there.

    If a user specifies a valid command, but for some reason the developer did not register it, an AttributeError will  # noqa: E501
    raise, since it is a bug in this script.

    Finally, if a user specifies a valid command and it is registered with @command below, then that command is "chosen"  # noqa: E501
    by this decorator function, and set as the attribute `chosen`. It is then executed below in  # noqa: E501
    `if __name__ == '__main__':`.

    Doing this instead of using Flask-Script.

    Positional arguments:
    func -- the function to decorate
    """
    @wraps(func)
    def wrapped():
        return func()

    # Register chosen function.
    if func.__name__ not in OPTIONS:
        raise KeyError(
            ('Cannot register {}',
             'not mentioned in docstring/docopt.'.format(func.__name__)))
    if OPTIONS[func.__name__]:
        command.chosen = func

    return wrapped


@command
def shell():
    setup_logging('shell')
    app = create_app(OPTIONS['--env'], parse_options())
    app.app_context().push()
    db.init_app(app)
    Shell(
        make_context=lambda: dict(app=app, db=db))\
        .run(
            no_ipython=False, 
            no_bpython=False, 
            no_ptipython=False, 
            no_ptpython=False)

if __name__ == '__main__':
    # Properly handle Control+C
    signal.signal(signal.SIGINT, lambda *_: sys.exit(0))
    getattr(command, 'chosen')()  # Execute the function specified by the user
