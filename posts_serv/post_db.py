import time
from datetime import datetime
from typing import Optional

from sqlalchemy import create_engine, and_, or_, func
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import sessionmaker

from models import Base, Post, Comment
from proto import post_pb2


class PostDB:
    def __init__(self, db_url: str, retries: int = 5, delay: int = 5):
        self.engine = None
        self.Session = None
        for i in range(retries):
            try:
                self.engine = create_engine(db_url)
                self.Session = sessionmaker(bind=self.engine)
                Base.metadata.drop_all(self.engine)
                Base.metadata.create_all(self.engine)
                break
            except OperationalError:
                if i == retries - 1:
                    raise RuntimeError("Failed to connect database")
                time.sleep(delay)

    def create_post(self, post_data: post_pb2.CreatePostRequest) -> post_pb2.CreatePostResponse:
        session = self.Session()
        try:
            new_post = Post(
                title=post_data.title,
                description=post_data.description,
                creator_id=post_data.creator_id,
                is_private=post_data.is_private,
                tags=post_data.tags
            )
            session.add(new_post)
            session.commit()

            return post_pb2.CreatePostResponse(
                post_id=str(new_post.post_id),
                created_at=new_post.created_at.isoformat()
            )
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def get_post(self, post_id: str, user_id: str) -> Optional[post_pb2.GetPostResponse]:
        session = self.Session()
        try:
            post = session.query(Post).filter(
                and_(
                    Post.post_id == int(post_id),
                    or_(Post.is_private == False, Post.creator_id == user_id)
                )
            ).first()

            if not post:
                return None

            return post_pb2.GetPostResponse(
                post=post_pb2.Post(
                    post_id=str(post.post_id),
                    title=post.title,
                    description=post.description,
                    creator_id=post.creator_id,
                    created_at=post.created_at.isoformat(),
                    updated_at=post.updated_at.isoformat(),
                    is_private=post.is_private,
                    tags=post.tags
                )
            )
        except Exception:
            raise
        finally:
            session.close()

    def update_post(self, post_data: post_pb2.UpdatePostRequest) -> Optional[post_pb2.UpdatePostResponse]:
        session = self.Session()
        try:
            post = session.query(Post).filter(
                and_(
                    Post.post_id == int(post_data.post_id),
                    Post.creator_id == post_data.user_id
                )
            ).first()

            if not post:
                raise

            if post_data.title:
                post.title = post_data.title
            if post_data.description:
                post.description = post_data.description
            if post_data.tags:
                post.tags = post_data.tags
            post.is_private = post_data.is_private

            session.commit()

            return post_pb2.UpdatePostResponse(
                updated_at=post.updated_at.isoformat()
            )
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_post(self, post_id: str, user_id: str) -> bool:
        session = self.Session()
        try:
            result = session.query(Post).filter(
                and_(
                    Post.post_id == int(post_id),
                    Post.creator_id == user_id
                )
            ).delete()

            session.commit()
            return result > 0
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def list_posts(self, user_id: str, page: int, per_page: int) -> post_pb2.ListPostsResponse:
        session = self.Session()
        try:
            total = session.query(func.count(Post.post_id)).filter(
                or_(
                    Post.is_private == False,
                    Post.creator_id == user_id
                )
            ).scalar()

            last_page = (total + per_page - 1) // per_page if per_page > 0 else 1
            current_page = max(min(page, last_page), 1) if total > 0 else 1
            offset = (current_page - 1) * per_page
            from_ = offset + 1 if total > 0 else 0
            to_ = min(offset + per_page, total)

            posts = session.query(Post).filter(
                or_(
                    Post.is_private == False,
                    Post.creator_id == user_id
                )
            ).order_by(Post.created_at.asc()).limit(per_page).offset(offset).all()

            return post_pb2.ListPostsResponse(
                posts=[self._post_to_list_pb(post) for post in posts],
                total=total,
                page=current_page,
                per_page=per_page,
                last_page=last_page,
                from_=from_,
                to_=to_
            )
        except SQLAlchemyError:
            raise
        finally:
            session.close()

    def create_comment(self, comment_data: post_pb2.CommentPostRequest) -> post_pb2.CommentPostResponse:
        session = self.Session()
        try:
            self._check_post_access(session, int(comment_data.post_id), comment_data.user_id)

            new_comment = Comment(
                post_id=int(comment_data.post_id),
                user_id=comment_data.user_id,
                text=comment_data.comment,
                created_at=datetime.utcnow()
            )
            session.add(new_comment)
            session.flush()
            session.commit()

            return post_pb2.CommentPostResponse(
                comment_id=str(new_comment.comment_id),
                created_at=new_comment.created_at.isoformat()
            )
        except Exception:
            raise
        finally:
            session.close()

    def list_comments(self, post_id: str, user_id: str, page: int, per_page: int) -> post_pb2.ListCommentsResponse:
        session = self.Session()
        try:
            if page <= 0 or per_page <= 0:
                raise

            self._check_post_access(session, int(post_id), user_id)

            total = session.query(func.count(Comment.comment_id)).filter(Comment.post_id == int(post_id)).scalar()

            if total == 0:
                return post_pb2.ListCommentsResponse(
                    comments=[],
                    meta=post_pb2.Meta(
                        total=0,
                        page=page,
                        per_page=per_page,
                        last_page=1
                    )
                )

            last_page = (total + per_page - 1) // per_page
            if page > last_page:
                raise

            offset = (page - 1) * per_page
            comments = session.query(Comment).filter(Comment.post_id == int(post_id)).order_by(
                Comment.created_at.asc()).limit(per_page).offset(offset).all()

            comments_list = [
                post_pb2.Comment(
                    comment_id=str(comment.comment_id),
                    text=comment.text,
                    user_id=comment.user_id,
                    created_at=comment.created_at.isoformat()
                )
                for comment in comments
            ]

            meta_pb = post_pb2.Meta(
                total=total,
                page=page,
                per_page=per_page,
                last_page=last_page
            )

            return post_pb2.ListCommentsResponse(
                comments=comments_list,
                meta=meta_pb
            )
        except Exception:
            raise
        finally:
            session.close()

    def _post_to_list_pb(self, post: Post) -> post_pb2.Post:
        return post_pb2.Post(
            post_id=str(post.post_id),
            title=post.title,
            description=post.description,
            creator_id=post.creator_id,
            created_at=post.created_at.isoformat(),
            updated_at=post.updated_at.isoformat() if post.updated_at else "",
            is_private=post.is_private,
            tags=post.tags if post.tags else []
        )

    def _check_post_access(self, session, post_id: int, user_id: str) -> Post:
        post = session.query(Post).get(post_id)
        if not post:
            raise
        if post.is_private and post.creator_id != user_id:
            raise
        return post

    def close(self):
        if self.engine:
            self.engine.dispose()
