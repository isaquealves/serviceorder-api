"""Manage script to start some services
@See https://github.com/Robpol86/Flask-Large-Application-Example from I took some implementation ideas. 
And remember: never just copy/paste, make some effort writing things, so you get to understand the basic concepts.

License: MIT

Command details:
    shell               Starts a Python interactive shell with the Flask
                        application context.

Usage:
    manage.py shell [--env=ENV]
    manage.py (-h | --help)
    manage.py celerydev
    manage.py celerybeat [-s FILE] [--pid=FILE] 
    manage.py celeryworker [-n NUM]

Options:
    --env=ENV                   Load the configuration based on environment.

    -n NUM --name=NUM           Celery Worker name integer.
                                [default: 1]
    --pid=FILE                  Celery Beat PID file.
                                [default: ./celery_beat.pid]
    -p NUM --port=NUM           Flask will listen on this port number.
                                [default: 5000]
    -s FILE --schedule=FILE     Celery Beat schedule database file.
"""
from __future__ import print_function
from functools import wraps
import logging
import logging.handlers
import signal
import sys

from docopt import docopt
from flask_script import Shell
from celery.bin.celery import main as celery_main

from app import create_app, get_config
from app.providers.database import db

OPTIONS = docopt(__doc__) if __name__ == '__main__' else dict()


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
            (f'Cannot register {func.__name__}',
             'not mentioned in docstring/docopt.'))
    if OPTIONS[func.__name__]:
        command.chosen = func

    return wrapped


@command
def celerydev():
    env = OPTIONS['--env'] or 'dev'
    app = create_app(env, parse_options())
    celery_args = [
        'celery', 'worker', '-B', '-E',
        '-s', '/tmp/celery.db', '--concurrency=5', '--loglevel=DEBUG']  # nosec
    with app.app_context():
        return celery_main(celery_args)


@command
def celerybeat():
    env = OPTIONS['--env'] or 'dev'
    pidfile = OPTIONS['--pid'] or './celery.pid'
    schedule = OPTIONS['--schedule'] or './celery-beat.db'
    app = create_app(env, parse_options())
    celery_args = [
        'celery', 'beat', '-C', '--pidfile',
        pidfile, '-s', schedule]
    with app.app_context():
        return celery_main(celery_args)


@command
def celeryworker():
    env = OPTIONS['--env'] or 'dev'
    cname = OPTIONS['--name'] or 123
    app = create_app(env, parse_options())
    celery_args = [
        'celery', 'worker', '-n', cname,
        '-C', '--autoscale=10,1', '--without-gossip']
    with app.app_context():
        return celery_main(celery_args)


@command
def shell():
    env = OPTIONS['--env'] or 'dev'
    app = create_app(env, parse_options())
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
