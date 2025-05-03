from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationError
from typing import List, Optional, Dict, Any
import re
from datetime import datetime
from collections import OrderedDict


class PostBase(BaseModel):
    description: Optional[str] = Field(None, max_length=1000)
    is_private: Optional[bool] = None
    tags: Optional[List[str]] = Field(None)

    @field_validator('tags')
    def validate_tags(cls, v):
        if v is not None and len(v) > 10:
            raise ValueError("Maximum 10 tags allowed")
        return v

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()},
        populate_by_name=True
    )


class PostCreate(PostBase):
    title: str = Field(..., min_length=1, max_length=100)


class PostUpdate(PostBase):
    title: Optional[str] = Field(None, min_length=1, max_length=100)


class PostResponse(PostBase):
    post_id: int
    title: str
    description: str
    creator_id: str
    created_at: str
    updated_at: str
    is_private: bool
    tags: List[str]

    def dict(self, **kwargs) -> Dict[str, Any]:
        return OrderedDict([
            ("post_id", self.post_id),
            ("title", self.title),
            ("description", self.description),
            ("creator_id", self.creator_id),
            ("created_at", self.created_at),
            ("updated_at", self.updated_at),
            ("is_private", self.is_private),
            ("tags", self.tags)
        ])


class ListQuery(BaseModel):
    page: int = Field(1, gt=0)
    per_page: int = Field(10, gt=0, le=100)

class CommentCreation(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)


class ListPostsResponse(BaseModel):
    posts: List[PostResponse]

    def dict(self, **kwargs) -> Dict[str, Any]:
        return OrderedDict([
            ("posts", [post.dict() for post in self.posts]),
            ("meta", self.meta.dict())
        ])


def validate_post_id(post_id: str) -> int:
    if not re.match(r'^\d+$', post_id):
        raise Exception("Post ID must be a positive integer")
    return int(post_id)
