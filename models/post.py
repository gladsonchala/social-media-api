from pydantic import BaseModel

class UserPostIn(BaseModel):
    body: str
    user_id: int

class UserPost(UserPostIn):
    id: int

class CommentIn(BaseModel):
    body: str
    post_id: int

class Comment(CommentIn):
    id: int
    user_id: int

class UserPostWithComments(UserPost):
    comments: list[Comment]
