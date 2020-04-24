import inspect
import app
import pudb
def test_has_create_app():
    assert hasattr(app, 'create_app')

def test_create_app_receive_env_args():
    assert 'env' in inspect.signature(app.create_app).parameters.keys()

def test_create_app_receive_settings_args():
    assert 'additional_settings' in inspect.signature(app.create_app).parameters.keys()