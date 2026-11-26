'''
models
defines sql alchemy data models
also contains the definition for the room class used to keep track of socket.io rooms
'''

# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, Column, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, declarative_base
from typing import Dict


# class User:
#     def __init__(self, private_key, public_key):
#         self.private_key = private_key
#         self.public_key = public_key

# # data models
# class Base(declarative_base):
#     pass

Base = declarative_base()

# model to store user information
class User(Base):
    __tablename__ = "user"
    
    # username: Mapped[str] = mapped_column(String, primary_key=True)
    # password: Mapped[str] = mapped_column(String)
    # logged_in: Mapped[bool] = mapped_column(Boolean, default=False)
    # is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    # is_muted: Mapped[bool] = mapped_column(Boolean, default=False)
    
    username = Column(String, primary_key=True)
    password = Column(String)
    logged_in = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_muted = Column(Boolean, default=False)

# model to store friends information
class Friend(Base):
    __tablename__ = 'friends'
    
    id = Column(Integer, primary_key=True)
    user_username = Column(String, ForeignKey('user.username'))
    friend_username = Column(String, ForeignKey('user.username'))

    user = relationship("User", foreign_keys=[user_username])
    friend = relationship("User", foreign_keys=[friend_username])

class Category(Base):
    __tablename__ = 'category'

    name = Column(String, primary_key = True)

# model to store posts
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key = True)
    username = Column(String, ForeignKey('user.username'))
    title = Column(String)
    content = Column(String)
    post_category = Column(String, ForeignKey('category.name'))
    time = Column(DateTime)

    user = relationship("User", foreign_keys=[username])
    category = relationship("Category", foreign_keys=[post_category])


# stateful counter used to generate the room id
class Counter():
    def __init__(self):
        self.counter = 0
    
    def get(self):
        self.counter += 1
        return self.counter


class Room():
    def __init__(self):
        self.counter = Counter()
        self.dict: Dict[str, int] = {}
        self.friend_pk = None

    def create_room(self, sender: str, receiver: str) -> int:
        room_id = self.counter.get()
        self.dict[sender] = room_id
        self.dict[receiver] = room_id
        return room_id
    
    def join_room(self,  sender: str, room_id: int) -> int:
        self.dict[sender] = room_id

    def leave_room(self, user):
        if user not in self.dict.keys():
            return
        del self.dict[user]

    def get_room_id(self, user: str):
        if user not in self.dict.keys():
            return None
        return self.dict[user]
    
    def set_friend_pk(self, pk):
        # TODO: check if pk is valid
        self.friend_pk = pk

    def get_friend_pk(self):
        # check needed
        return self.friend_pk