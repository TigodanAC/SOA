from flask import Flask, request, jsonify, g, Response
import requests
import grpc
import json
from collections import OrderedDict
from auth import token_required
from schemas import (
    PostCreate,
    PostUpdate,
    PostResponse,
    ListPostsQuery,
    validate_post_id,
)
from proto import post_pb2, post_pb2_grpc

USER_SERVICE_URL = "http://user_service:5000"
POST_SERVICE_URL = "post_service:50051"

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['USER_SERVICE_URL'] = USER_SERVICE_URL

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/register', methods=['POST'])
def register():
    try:
        response = requests.post(f"{USER_SERVICE_URL}/register", json=request.json)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"message": f"Internal server error: {e}"}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        response = requests.post(f"{USER_SERVICE_URL}/login", json=request.json)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"message": f"Internal server error: {e}"}), 500


@app.route('/profile', methods=['GET'])
def get_profile():
    try:
        response = requests.get(f"{USER_SERVICE_URL}/profile", headers=request.headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"message": f"Internal server error: {e}"}), 500


@app.route('/profile', methods=['PUT'])
def update_profile():
    try:
        response = requests.put(f"{USER_SERVICE_URL}/profile", headers=request.headers, json=request.json)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"message": f"Internal server error: {e}"}), 500



def get_grpc_stub():
    if "grpc_stub" not in g:
        channel = grpc.insecure_channel(f"{POST_SERVICE_URL}")
        g.grpc_stub = post_pb2_grpc.PostServiceStub(channel)
    return g.grpc_stub


def handle_grpc_error(error: grpc.RpcError):
    error_message = error.details()
    if error.code() == grpc.StatusCode.OUT_OF_RANGE:
        return jsonify({"message": error_message}), 400
    error_map = {
        grpc.StatusCode.NOT_FOUND: (404, error_message),
        grpc.StatusCode.PERMISSION_DENIED: (403, error_message),
        grpc.StatusCode.INVALID_ARGUMENT: (400, error_message),
        grpc.StatusCode.UNAUTHENTICATED: (401, error_message),
        grpc.StatusCode.INTERNAL: (500, error_message)
    }
    status_code, message = error_map.get(error.code(), (500, "Internal server error"))
    return jsonify({"message": message}), status_code


@app.route('/posts', methods=['POST'])
@token_required
def create_post(user_id: str):
    try:
        data = PostCreate(**request.get_json())
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 400

    try:
        grpc_request = post_pb2.CreatePostRequest(
            title=data.title,
            description=data.description,
            creator_id=user_id,
            is_private=data.is_private,
            tags=data.tags
        )
        stub = get_grpc_stub()
        response = stub.CreatePost(grpc_request)
        return jsonify({
            "post_id": response.post_id,
            "created_at": response.created_at
        }), 201
    except grpc.RpcError as e:
        return handle_grpc_error(e)


@app.route('/posts/<post_id>', methods=['GET'])
@token_required
def get_post(user_id: str, post_id: str):
    try:
        post_id = validate_post_id(post_id)
        grpc_request = post_pb2.GetPostRequest(
            post_id=str(post_id),
            user_id=user_id
        )
        stub = get_grpc_stub()
        response = stub.GetPost(grpc_request)

        if not response.HasField('post'):
            return jsonify({"message": "Post didn't found"}), 404

        data = OrderedDict([
            ("post_id", int(response.post.post_id)),
            ("title", response.post.title),
            ("description", response.post.description),
            ("creator_id", response.post.creator_id),
            ("created_at", response.post.created_at),
            ("updated_at", response.post.updated_at),
            ("is_private", response.post.is_private),
            ("tags", list(response.post.tags))
        ])
        return json.dumps(data, ensure_ascii=False), 200, {'Content-Type': 'application/json'}

    except grpc.RpcError as e:
        return handle_grpc_error(e)
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 400


@app.route('/posts/<post_id>', methods=['PUT'])
@token_required
def update_post(user_id: str, post_id: str):
    try:
        post_id = validate_post_id(post_id)
        data = PostUpdate(**request.get_json())
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 400

    try:
        update_fields = {}
        if data.title is not None:
            update_fields['title'] = data.title
        if data.description is not None:
            update_fields['description'] = data.description
        if data.is_private is not None:
            update_fields['is_private'] = data.is_private
        if data.tags is not None:
            update_fields['tags'] = data.tags

        grpc_request = post_pb2.UpdatePostRequest(
            post_id=str(post_id),
            user_id=user_id,
            **update_fields
        )

        stub = get_grpc_stub()
        response = stub.UpdatePost(grpc_request)
        return jsonify({"updated_at": response.updated_at}), 200

    except grpc.RpcError as e:
        return handle_grpc_error(e)
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 400


@app.route('/posts/<post_id>', methods=['DELETE'])
@token_required
def delete_post(user_id: str, post_id: str):
    try:
        post_id = validate_post_id(post_id)
        grpc_request = post_pb2.DeletePostRequest(
            post_id=str(post_id),
            user_id=user_id
        )
        stub = get_grpc_stub()
        _ = stub.DeletePost(grpc_request)
        return jsonify({"message": "Post deleted successfully."}), 200

    except grpc.RpcError as e:
        return handle_grpc_error(e)
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 400


@app.route('/posts', methods=['GET'])
@token_required
def list_posts(user_id: str):
    try:
        query = ListPostsQuery(
            page=request.args.get('page', 1, type=int),
            per_page=request.args.get('per_page', 10, type=int)
        )
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 400

    try:
        grpc_request = post_pb2.ListPostsRequest(
            user_id=user_id,
            page=query.page,
            per_page=query.per_page
        )
        stub = get_grpc_stub()
        response = stub.ListPosts(grpc_request)

        posts = [
            PostResponse(
                post_id=int(post.post_id),
                title=post.title,
                description=post.description,
                creator_id=post.creator_id,
                created_at=post.created_at,
                updated_at=post.updated_at,
                is_private=post.is_private,
                tags=list(post.tags)
            ).dict()
            for post in response.posts
        ]

        return Response(
            json.dumps({"posts": posts}, ensure_ascii=False, sort_keys=False),
            mimetype='application/json'
        ), 200

    except grpc.RpcError as e:
        return handle_grpc_error(e)
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
