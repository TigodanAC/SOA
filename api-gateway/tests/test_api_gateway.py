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
    global TOKEN
    login_response = client.post('/login', json={
        "login": "john_doe",
        "password": "password@123"
    })
    TOKEN = login_response.json["token"]
    assert client.get('/profile', headers={"Authorization": TOKEN}).json['email'] == "john@doe.com"

    login_response = client.post('/login', json={
        "login": "new_john_doe",
        "password": "password@123"
    })
    assert login_response.status_code == 401
    assert login_response.json == {"message": "Invalid credentials"}

@pytest.mark.dependency(depends=["test_login_api"])
def test_profile_api(client):
    update_response = client.put('/profile', headers={"Authorization": TOKEN}, json={
        "first_name": "John",
        "second_name": "Doe",
        "profile": {
            "avatar": "http://avatar.jpg",
            "description": "I'm John, John Doe"
        }
    })
    assert update_response.status_code == 200
    assert update_response.json == {"message": "Profile updated successfully"}
    assert client.get('/profile', headers={"Authorization": TOKEN}).json['first_name'] == "John"

    update_response = client.put('/profile', headers={"Authorization": TOKEN}, json={
        "login": "new_john_doe",
        "password": "password@1234"
    })
    assert update_response.status_code == 400
    assert update_response.json == {"message": "Updating login or password is not allowed"}
    assert client.get('/profile', headers={"Authorization": TOKEN}).json['login'] == "john_doe"



@pytest.mark.dependency(depends=["test_login_api"])
def test_create_post_api(client):
    global POST_CREATED_ID
    response = client.post(
        '/posts',
        headers={"Authorization": TOKEN},
        json={
            "title": "Post",
            "description": "Description",
            "is_private": False,
            "tags": ["test"]
        }
    )
    data = response.get_json()
    assert response.status_code == 201
    assert "post_id" in data
    assert "created_at" in data

    POST_CREATED_ID = data["post_id"]
    response = client.post(
        '/posts',
        headers={"Authorization": TOKEN},
        json={
            "description": "Description",
            "is_private": False
        }
    )
    assert response.status_code == 400


@pytest.mark.dependency(depends=["test_create_post_api"])
def test_get_post_api(client):
    response = client.get(
        f'/posts/{POST_CREATED_ID}',
        headers={"Authorization": TOKEN}
    )
    data = response.get_json()
    assert response.status_code == 200
    assert data["post_id"] == int(POST_CREATED_ID)
    assert data["title"] == "Post"
    assert data["description"] == "Description"
    assert data["is_private"] is False
    assert data["tags"] == ["test"]


@pytest.mark.dependency(depends=["test_create_post_api"])
def test_update_post_api(client):
    response = client.put(
        f'/posts/{POST_CREATED_ID}',
        headers={"Authorization": TOKEN},
        json={
            "title": "Updated Title",
            "description": "Updated description",
            "is_private": True
        }
    )
    data = response.get_json()
    assert response.status_code == 200
    assert "updated_at" in data

    response = client.get(
        f'/posts/{POST_CREATED_ID}',
        headers={"Authorization": TOKEN}
    )
    data = response.get_json()
    assert response.status_code == 200
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated description"
    assert data["is_private"] is True


@pytest.mark.dependency(depends=["test_login_api"])
def test_list_posts_api(client):
    response = client.get(
        '/posts?page=1&per_page=5',
        headers={"Authorization": TOKEN}
    )
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    assert "posts" in response.get_json()


@pytest.mark.dependency(depends=["test_update_post_api"])
def test_delete_post_api(client):
    response = client.delete(
        f'/posts/{POST_CREATED_ID}',
        headers={"Authorization": TOKEN}
    )
    assert response.status_code == 200
    assert response.get_json()["message"] == "Post deleted successfully."

    get_response = client.get(
        f'/posts/{POST_CREATED_ID}',
        headers={"Authorization": TOKEN}
    )
    assert get_response.status_code == 404


def test_protected_posts(client):
    response = client.get(
        '/posts',
        headers={"Authorization": "some.invalid.token"}
    )
    assert response.status_code == 401


@pytest.mark.dependency(depends=["test_create_post_api"])
def test_post_pagination_boundaries(client):
    response = client.get(
        '/posts?page=0&per_page=0',
        headers={"Authorization": TOKEN}
    )
    assert response.status_code == 400

    response = client.get(
        '/posts?page=1&per_page=101',
        headers={"Authorization": TOKEN}
    )
    assert response.status_code == 400



@pytest.fixture(scope="session", autouse=True)
def cleanup_after_tests():
    yield
    app.config['TESTING'] = False