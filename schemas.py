from pydantic import BaseModel
from typing import  Optional
from datetime import date as date_type

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


class Leaves(BaseModel):
    leave_date: date_type
    leave_type: str      # fullday or halfday

class Leaves_response(BaseModel):
    leave_date: str
    leave_type: str      # fullday or halfday

