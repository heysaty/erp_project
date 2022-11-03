import enum
from sqlalchemy import Column, Integer, ForeignKey, String, Enum
from sqlalchemy.orm import relationship
from database import Base


# from sqlalchemy import Integer, Enum
#
# class MyEnum(enum.Enum):
#     one = 1
#     two = 2
#     three = 3


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String)

    user_leaves = relationship("Leaves", back_populates='leave_user')

    token_receiver = relationship("Tokens", back_populates='token_sender')


class Leaves(Base):
    __tablename__ = 'leaves'

    id = Column(Integer, primary_key=True, index=True)
    leave_type = Column(String)
    leave_status = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    leave_user = relationship("User", back_populates='user_leaves')


class Tokens(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    token = Column(String)

    token_sender = relationship("User", back_populates='token_receiver')
