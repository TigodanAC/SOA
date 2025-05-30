import grpc
from broker.kafka_producer import kafka_producer

from post_db import PostDB
from proto import post_pb2
from proto import post_pb2_grpc


class PostServiceServicer(post_pb2_grpc.PostServiceServicer):
    def __init__(self, db: PostDB):
        self.db = db

    def CreatePost(self, request, context):
        try:
            response = self.db.create_post(request)
            return response
        except Exception:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return post_pb2.CreatePostResponse()

    def DeletePost(self, request, context):
        try:
            response = self.db.delete_post(request.post_id, request.user_id)
            if response:
                return post_pb2.DeletePostResponse(success=True)
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Post not found or permission denied")
                return post_pb2.DeletePostResponse()
        except Exception:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return post_pb2.DeletePostResponse()

    def UpdatePost(self, request, context):
        try:
            response = self.db.update_post(request)
            if response:
                return response
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Post not found or permission denied")
                return post_pb2.UpdatePostResponse()
        except Exception:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return post_pb2.UpdatePostResponse()

    def GetPost(self, request, context):
        try:
            response = self.db.get_post(request.post_id, request.user_id)
            if response and response.post:
                return response
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Post not found")
                return post_pb2.GetPostResponse()
        except Exception:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return post_pb2.GetPostResponse()

    def ListPosts(self, request, context):
        try:
            response = self.db.list_posts(
                user_id=request.user_id,
                page=request.page,
                per_page=request.per_page
            )
            return response
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return post_pb2.ListPostsResponse()
        except Exception:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return post_pb2.ListPostsResponse()

    def ViewPost(self, request, context):
        try:
            kafka_producer.send_post_viewed_event(request.user_id, request.post_id)
            return post_pb2.ViewPostResponse(success=True)
        except Exception:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return post_pb2.ViewPostResponse()

    def LikePost(self, request, context):
        try:
            kafka_producer.send_post_liked_event(request.user_id, request.post_id)
            return post_pb2.LikePostResponse(success=True)
        except Exception:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return post_pb2.LikePostResponse()

    def CommentPost(self, request, context):
        try:
            result = self.db.create_comment(request)
            kafka_producer.send_post_commented_event(
                user_id=request.user_id,
                post_id=request.post_id,
                comment_id=result.comment_id,
                text=request.comment[:100]
            )
            return result
        except Exception:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return post_pb2.CommentPostResponse()

    def ListComments(self, request, context):
        try:
            return self.db.list_comments(
                request.post_id,
                request.user_id,
                request.page,
                request.per_page
            )
        except Exception:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return post_pb2.ListCommentsResponse()
