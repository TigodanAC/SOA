import pytest
from sqlalchemy import Integer, String, Text, Boolean, DateTime, ARRAY
from models import Post


@pytest.fixture
def sample_post():
    title = "Post"
    description = "Description"
    creator_id = "User"
    tags = ["test", "db"]
    post = Post(
        title=title,
        description=description,
        creator_id=creator_id,
        is_private=False,
        tags=tags
    )
    return post


def test_post_instance_fields(sample_post):
    assert sample_post.title == "Post"
    assert sample_post.description == "Description"
    assert sample_post.creator_id == "User"
    assert sample_post.is_private is False
    assert sample_post.tags == ["test", "db"]


def test_post_column_definitions():
    columns = Post.__table__.columns
    assert isinstance(columns['post_id'].type, Integer)
    assert columns['post_id'].primary_key is True
    assert isinstance(columns['title'].type, String)
    assert columns['title'].nullable is False
    assert isinstance(columns['description'].type, Text)
    assert isinstance(columns['creator_id'].type, String)
    assert columns['creator_id'].nullable is False
    assert isinstance(columns['created_at'].type, DateTime)
    assert callable(columns['created_at'].default.arg)
    assert isinstance(columns['updated_at'].type, DateTime)
    assert callable(columns['updated_at'].default.arg)
    assert isinstance(columns['is_private'].type, Boolean)
    assert columns['is_private'].default.arg is False
    assert isinstance(columns['tags'].type, ARRAY)
    assert columns['tags'].default.arg == []
