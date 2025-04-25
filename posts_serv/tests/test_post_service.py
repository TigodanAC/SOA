import pytest
from unittest.mock import MagicMock
import grpc
from datetime import datetime
from proto import post_pb2
from post_grpc_service import PostServiceServicer
from sqlalchemy.exc import SQLAlchemyError


class DummyContext:
    def __init__(self):
        self.code = None
        self.details = None

    def set_code(self, code):
        self.code = code

    def set_details(self, details):
        self.details = details


@pytest.fixture
def dummy_context():
    return DummyContext()


@pytest.fixture
def servicer():
    mock_db = MagicMock()
    return PostServiceServicer(mock_db), mock_db


def test_create_post_success(servicer, dummy_context):
    service, mock_db = servicer
    mock_db.create_post.return_value = post_pb2.CreatePostResponse(post_id="1",
                                                                   created_at=datetime.utcnow().isoformat())
    request = post_pb2.CreatePostRequest(
        title="Post",
        description="Description",
        creator_id="User",
        is_private=False,
        tags=["test"]
    )
    response = service.CreatePost(request, dummy_context)
    assert response.post_id == "1"
    assert dummy_context.code is None


def test_create_post_db_error(servicer, dummy_context):
    service, mock_db = servicer
    mock_db.create_post.side_effect = SQLAlchemyError("DB error")
    request = post_pb2.CreatePostRequest(
        title="Post",
        description="Description",
        creator_id="User",
        is_private=False,
        tags=["test"]
    )
    _ = service.CreatePost(request, dummy_context)
    assert dummy_context.code == grpc.StatusCode.INTERNAL


def test_delete_post_success(servicer, dummy_context):
    service, mock_db = servicer
    mock_db.delete_post.return_value = True
    request = post_pb2.DeletePostRequest(
        post_id="1",
        user_id="User"
    )
    response = service.DeletePost(request, dummy_context)
    assert response.success is True
    assert dummy_context.code is None


def test_delete_post_not_found(servicer, dummy_context):
    service, mock_db = servicer
    mock_db.delete_post.return_value = False
    request = post_pb2.DeletePostRequest(
        post_id="1",
        user_id="User"
    )
    _ = service.DeletePost(request, dummy_context)
    assert dummy_context.code == grpc.StatusCode.NOT_FOUND
    assert dummy_context.details == "Post not found or permission denied"


def test_update_post_success(servicer, dummy_context):
    service, mock_db = servicer
    mock_db.update_post.return_value = post_pb2.UpdatePostResponse(updated_at=datetime.utcnow().isoformat())
    request = post_pb2.UpdatePostRequest(
        post_id="1",
        user_id="User",
        title="Updated Post",
        description="Updated Description",
        is_private=True,
        tags=["update"]
    )
    response = service.UpdatePost(request, dummy_context)
    assert hasattr(response, "updated_at")
    assert dummy_context.code is None


def test_update_post_not_found(servicer, dummy_context):
    service, mock_db = servicer
    mock_db.update_post.return_value = None
    request = post_pb2.UpdatePostRequest(
        post_id="1",
        user_id="User",
        title="Updated Post",
        description="Updated Description",
        is_private=True,
        tags=["update"]
    )
    _ = service.UpdatePost(request, dummy_context)
    assert dummy_context.code == grpc.StatusCode.NOT_FOUND
    assert dummy_context.details == "Post not found or permission denied"


def test_get_post_success(servicer, dummy_context):
    service, mock_db = servicer
    mock_db.get_post.return_value = post_pb2.GetPostResponse(post=post_pb2.Post(
        post_id="1",
        title="Post",
        description="Description",
        creator_id="User",
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat(),
        is_private=False,
        tags=["test"]
    ))
    request = post_pb2.GetPostRequest(
        post_id="1",
        user_id="User"
    )
    response = service.GetPost(request, dummy_context)
    assert response.HasField("post")
    assert response.post.title == "Post"
    assert dummy_context.code is None


def test_get_post_not_found(servicer, dummy_context):
    service, mock_db = servicer
    mock_db.get_post.return_value = None
    request = post_pb2.GetPostRequest(
        post_id="1",
        user_id="User"
    )
    _ = service.GetPost(request, dummy_context)
    assert dummy_context.code == grpc.StatusCode.NOT_FOUND
    assert dummy_context.details == "Post not found"


def test_list_posts_success(servicer, dummy_context):
    service, mock_db = servicer
    posts = [post_pb2.Post(
        post_id=str(i), title=f"Post {i}", creator_id="User", created_at=datetime.utcnow().isoformat(),
        is_private=False
    ) for i in range(1, 6)]
    mock_db.list_posts.return_value = post_pb2.ListPostsResponse(
        posts=posts,
        total=10,
        page=1,
        per_page=5,
        last_page=2,
        from_=1,
        to_=5
    )
    request = post_pb2.ListPostsRequest(
        user_id="User",
        page=1,
        per_page=5
    )
    response = service.ListPosts(request, dummy_context)
    assert response.total == 10
    assert response.page == 1
    assert len(response.posts) == 5
    assert dummy_context.code is None
