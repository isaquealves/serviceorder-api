
def test_root(client):
    response = client.get('/v1/')

    expected = {
        'message': 'Welcome to Service order api'
    }
    assert expected == response.json