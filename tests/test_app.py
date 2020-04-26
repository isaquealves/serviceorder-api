
import inspect
import app


def test_has_create_app():
    assert hasattr(app, 'create_app')  # nosec


def test_create_app_receive_env_args():
    args = inspect.signature(app.create_app).parameters.keys()
    assert 'env' in args  # nosec


def test_create_app_receive_settings_args():
    args = inspect.signature(app.create_app).parameters.keys()
    assert 'config' in args  # nosec
