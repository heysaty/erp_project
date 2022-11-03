from pydantic import BaseModel
from typing import  Optional


# pydantic model are called schema
# these are response model

class ShowUser(BaseModel):
    email: str
    role: str
    password: str

    class Config():
        orm_mode = True

    pass


class User(ShowUser):
    first_name: str
    last_name: str


    class Config():
        orm_mode = True

    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
