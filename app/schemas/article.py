from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from .user import UserResponse

class ArticleBase(BaseModel):
    title: str
    description: str
    body: str

class ArticleCreate(ArticleBase):
    tag_list: Optional[List[str]] = []

class ArticleResponse(ArticleBase):
    id: int
    slug: str
    author: UserResponse

    class Config(ConfigDict):
        from_attributes = True

class TagResponse(BaseModel):
    name: str

    class Config(ConfigDict):
        from_attributes = True