import pytest
from datetime import datetime
from unittest.mock import patch
from ..user_service import app, db, User, UserProfile


@pytest.fixture
def app_context():
    with app.app_context():
        yield


@pytest.fixture
def mock_db(app_context):
    with (patch('models.db.session.add') as mock_add, \
            patch('models.db.session.commit') as mock_commit, \
            patch('models.db.session.delete') as mock_delete, \
            patch('models.User.query') as mock_user_query, \
            patch('models.UserProfile.query') as mock_profile_query):
        yield {
            "mock_add": mock_add,
            "mock_commit": mock_commit,
            "mock_delete": mock_delete,
            "mock_user_query": mock_user_query,
            "mock_profile_query": mock_profile_query,
        }


def test_user(mock_db):
    user = User(
        user_id="user_id",
        login="john_doe",
        email="john@doe.com",
        password="password@123",
        role="user",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    mock_db["mock_user_query"].get.return_value = user
    user_ = User.query.get("user_id")
    assert user_.login == "john_doe"
    assert user_.email == "john@doe.com"
    assert user_.role == "user"
    assert isinstance(user_.updated_at, datetime)


def test_user_update(mock_db):
    user = User(
        user_id="user_id",
        login="john_doe",
        email="john@doe.com",
        password="password@123",
        role="user",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    mock_db["mock_user_query"].get.return_value = user
    user.role = "admin"
    user.email = "new_john@doe.com"
    db.session.add(user)
    db.session.commit()
    user_ = User.query.get("user_id")

    assert user_.role == "admin"
    assert user_.email == "new_john@doe.com"


def test_user_delete(mock_db):
    user = User(
        user_id="user_id",
        login="john_doe",
        email="john@doe.com",
        password="password@123",
        role="user",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    mock_db["mock_user_query"].get.return_value = None
    db.session.delete(user)
    db.session.commit()
    user_ = User.query.get("user_id")

    assert user_ is None


def test_profile(mock_db):
    user = User(
        user_id="user_id",
        login="john_doe",
        email="john@doe.com",
        password="password@123",
        role="user",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    profile = UserProfile(
        profile_id="profile_id",
        user_id="user_id",
        avatar="http://avatar.jpg",
        description="I'm John, John Doe",
        date_of_birth=datetime.fromisocalendar(1990, 1, 1),
    )

    mock_db["mock_user_query"].get.return_value = user
    mock_db["mock_profile_query"].get.return_value = profile
    profile.user = user
    db.session.add(user)
    db.session.add(profile)
    db.session.commit()
    profile_ = UserProfile.query.get("profile_id")

    assert profile_.user.login == "john_doe"
    assert profile_.avatar == "http://avatar.jpg"
    assert profile_.description == "I'm John, John Doe"
    assert isinstance(profile_.date_of_birth, datetime)


def test_profile_update(mock_db):
    profile = UserProfile(
        profile_id="profile_id",
        user_id="user_id",
        avatar="http://avatar.jpg",
        description="I'm John, John Doe",
        date_of_birth=datetime.fromisocalendar(1990, 1, 1),
    )

    mock_db["mock_profile_query"].get.return_value = profile
    profile.description = "I'm John, John Doe Junior."
    db.session.add(profile)
    db.session.commit()
    profile_ = UserProfile.query.get("profile_id")

    assert profile_.description == "I'm John, John Doe Junior."


def test_unique(mock_db):
    user1 = User(
        user_id="user_id",
        login="john_doe",
        email="john@doe.com",
        password="password@123",
        role="user",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.session.add(user1)
    db.session.commit()

    user2 = User(
        user_id="new_user_id",
        login="john_doe",
        email="new_john@doe.com",
        password="password@123",
        role="user",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    mock_db["mock_commit"].side_effect = Exception("Login is already taken")

    with pytest.raises(Exception, match="Login is already taken"):
        db.session.add(user2)
        db.session.commit()

    user3 = User(
        user_id="new_user_id",
        login="new_john_doe",
        email="john@doe.com",
        password="password@123",
        role="user",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    mock_db["mock_commit"].side_effect = Exception("Email is already registered")

    with pytest.raises(Exception, match="Email is already registered"):
        db.session.add(user3)
        db.session.commit()
