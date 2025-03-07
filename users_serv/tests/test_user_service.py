import pytest
from unittest.mock import patch
from ..user_service import app, User
from ..validity.validators import *


@pytest.fixture
def app_context():
    with app.app_context():
        yield


@pytest.fixture
def client(app_context):
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_db(app_context):
    with patch('models.db.session.add') as mock_add, \
            patch('models.db.session.commit') as mock_commit, \
            patch('models.db.session.delete') as mock_delete, \
            patch('models.User.query') as mock_user_query, \
            patch('models.UserProfile.query') as mock_profile_query:
        yield {
            "mock_add": mock_add,
            "mock_commit": mock_commit,
            "mock_delete": mock_delete,
            "mock_user_query": mock_user_query,
            "mock_profile_query": mock_profile_query,
        }


def test_register(mock_db):
    mock_db["mock_user_query"].filter_by.return_value.first.return_value = None
    response = app.test_client().post('/register', json={
        "login": "john_doe",
        "email": "john@doe.com",
        "password": "password@123",
    })

    assert response.status_code == 201
    assert response.json == {"message": "User registered successfully"}

    mock_db["mock_user_query"].filter_by.return_value.first.return_value = User(login="john_doe")
    response = app.test_client().post('/register', json={
        "login": "john_doe",
        "email": "john@doe.com",
        "password": "password@123",
    })

    assert response.status_code == 400
    assert response.json == {"message": "Login is already taken"}


def test_login(mock_db):
    user = User(
        user_id="user_id",
        login="john_doe",
        email="john@doe.com",
        password="password@123",
        role="user",
    )

    mock_db["mock_user_query"].filter_by.return_value.first.return_value = None
    response = app.test_client().post('/login', json={
        "login": "doe_john",
        "password": "Password123!"
    })

    assert response.status_code == 401
    assert response.json == {"message": "Invalid credentials"}

    mock_db["mock_user_query"].filter_by.return_value.first.return_value = user
    with patch('user_service.check_password_hash', return_value=False):
        response = app.test_client().post('/login', json={
            "login": "john_doe",
            "password": "123",
        })

    assert response.status_code == 401
    assert response.json == {"message": "Invalid credentials"}


@patch('user_service.decode_jwt')
def test_token(mock_decode, client):
    response = client.get('/profile')
    assert response.status_code == 401
    assert response.json == {"message": "Token is missing"}

    mock_decode.return_value = None
    response = client.get('/profile', headers={"Authorization": "invalid_token"})
    assert response.status_code == 401
    assert response.json == {"message": "Invalid or expired token"}


def test_validation():
    assert validate_login("john_doe") == (True, "")
    assert validate_login("john~doe") == (False, "Login can only contain letters, numbers, underscores, hyphens")
    assert validate_login("doe") == (False, "Login must be from 5 to 15 characters long")

    assert validate_email_format("john@doe.com") == (True, "")
    assert validate_email_format("johndoecom") == (False, "Invalid email format")

    assert validate_password("password@123") == (True, "")
    assert validate_password("d@1") == (False, "Password must be at least 4 characters long")
    assert validate_password("password123") == (False, "Password must contain at least one special character")
    assert validate_password("password@") == (False, "Password must contain at least one digit")

    assert validate_name("John") == (True, "")
    assert validate_name("John!") == (False, "Name can only contain letters, apostrophes, hyphens")

    assert validate_date_of_birth("1990-01-01") == (True, "")
    assert validate_date_of_birth("3023-01-01") == (False, "Date of birth cannot be in the future")
    assert validate_date_of_birth("27's of September, 2000") == (False, "Invalid date format")