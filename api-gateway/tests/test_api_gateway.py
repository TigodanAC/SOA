import pytest

from ..api_gateway import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.mark.dependency()
def test_register_api(client):
    response = client.post('/register', json={
        "login": "john_doe",
        "email": "john@doe.com",
        "password": "password@123",
    })
    assert response.status_code == 201
    assert response.json == {"message": "User registered successfully"}

    response = client.post('/register', json={
        "login": "john_doe",
        "email": "new_john@doe.com",
        "password": "password@123",
    })
    assert response.status_code == 400
    assert response.json == {"message": "Login is already taken"}

    response = client.post('/register', json={
        "login": "new_john_doe",
        "email": "john@doe.com",
        "password": "password@123",
    })
    assert response.status_code == 400
    assert response.json == {"message": "Email is already registered"}

@pytest.mark.dependency(depends=["test_register_api"])
def test_login_api(client):
    login_response = client.post('/login', json={
        "login": "john_doe",
        "password": "password@123"
    })
    token = login_response.json["token"]
    assert client.get('/profile', headers={"Authorization": token}).json['email'] == "john@doe.com"

    login_response = client.post('/login', json={
        "login": "new_john_doe",
        "password": "password@123"
    })
    assert login_response.status_code == 401
    assert login_response.json == {"message": "Invalid credentials"}

@pytest.mark.dependency(depends=["test_login_api"])
def test_profile_api(client):
    login_response = client.post('/login', json={
        "login": "john_doe",
        "password": "password@123"
    })
    token = login_response.json["token"]

    update_response = client.put('/profile', headers={"Authorization": token}, json={
        "first_name": "John",
        "second_name": "Doe",
        "profile": {
            "avatar": "http://avatar.jpg",
            "description": "I'm John, John Doe"
        }
    })
    assert update_response.status_code == 200
    assert update_response.json == {"message": "Profile updated successfully"}
    assert client.get('/profile', headers={"Authorization": token}).json['first_name'] == "John"

    update_response = client.put('/profile', headers={"Authorization": token}, json={
        "login": "new_john_doe",
        "password": "password@1234"
    })
    assert update_response.status_code == 400
    assert update_response.json == {"message": "Updating login or password is not allowed"}
    assert client.get('/profile', headers={"Authorization": token}).json['login'] == "john_doe"

@pytest.fixture(scope="session", autouse=True)
def cleanup_after_tests():
    yield
    app.config['TESTING'] = False