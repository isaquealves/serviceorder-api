from pathlib import Path

import pytest
from flask import current_app
from orator.migrations import DatabaseMigrationRepository, Migrator

from app import create_app, get_config
from app.providers.database import db as _db


@pytest.fixture(scope="session")
def app(request):
    """ Session wide test 'Flask' application """

    settings = get_config("app.settings.Testing")
    app = create_app(settings)
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.fixture
def client(app, db):
    return app.test_client()


@pytest.fixture(scope="session")
def db(app, request):
    """ Session-wide test database """
    migrations_path = Path(__file__).parent.parent.joinpath("migrations")
    with app.app_context():
        _db.init_app(current_app)
        repo = DatabaseMigrationRepository(_db, "migrations")
        migrator = Migrator(repo, _db)
        if not migrator.repository_exists():
            repo.create_repository()
        migrator.rollback(migrations_path)
        migrator.run(migrations_path)


@pytest.fixture(scope="function")
def db_scope_fn(app, request):
    """ Session-wide test database """
    migrations_path = Path(__file__).parent.parent.joinpath("migrations")
    with app.app_context():
        _db.init_app(current_app)
        repo = DatabaseMigrationRepository(_db, "migrations")
        migrator = Migrator(repo, _db)
        if not migrator.repository_exists():
            repo.create_repository()
        migrator.rollback(migrations_path)
        migrator.run(migrations_path)
