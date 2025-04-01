from concurrent import futures
import time
import grpc
from proto.post_pb2_grpc import add_PostServiceServicer_to_server
from post_grpc_service import PostServiceServicer
from post_db import PostDB
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def serve():
    server = None
    try:
        db = PostDB("postgresql://user:password@db:5432/post_db")
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
        add_PostServiceServicer_to_server(PostServiceServicer(db), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        while True:
            time.sleep(5)

    finally:
        if server:
            server.stop(0)
        db.close()


if __name__ == '__main__':
    serve()
