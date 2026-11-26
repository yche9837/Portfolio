'''
db
database file, containing all the logic to interface with the sql database
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import *
import datetime
from flask_sqlalchemy import SQLAlchemy

# "database/main.db" specifies the database file
# change it if you wish
# turn echo = True to display sql output
engine = create_engine("sqlite:///database/main.db", echo=False)

# initializes the database
Base.metadata.create_all(engine)

# inserts a user to the database
def insert_user(username: str, password: str):
    with Session(engine) as session:
        user = User(username=username, password=password)
        session.add(user)
        session.commit()

# login status setter
def login(username: str):
    with Session(engine) as session:
        user = session.get(User, username)
        user.logged_in = True
        session.commit()

# logout status setter
def logout(username: str):
    with Session(engine) as session:
        user = session.get(User, username)
        user.logged_in = False
        session.commit()

# gets login status
def get_login_status(username: str):
    with Session(engine) as session:
        user = session.get(User, username)
        return user.logged_in

# gets a user from the database
def get_user(username: str):
    with Session(engine) as session:
        return session.get(User, username)

# inserts a friend to the database
def insert_friend(user_username: str, friend_username: str):
    with Session(engine) as session:
        if not get_user(friend_username):
            return "Friend doesn't exist."
        stored_friend = session.query(Friend).filter(Friend.user_username == user_username, Friend.friend_username == friend_username).first()
        if stored_friend is not None:
            return "Friends already exists."
        friend = Friend(user_username=user_username, friend_username=friend_username)
        session.add(friend)
        session.commit()

# gets all friends of a user
def get_friends(username: str):
    with Session(engine) as session:
        return session.query(Friend).filter(Friend.user_username == username).all()

    
# gets all users in the database
def get_all_users():
    with Session(engine) as session:
        return session.query(User).all()
    
# login status setter
def set_admin(username: str):
    with Session(engine) as session:
        user = session.get(User, username)
        if user is not None:
            user.is_admin = True
        session.commit()

# checks whether the user is admin
def is_admin(username: str):
    with Session(engine) as session:
        user = session.get(User, username)
        if user is not None:
            return user.is_admin
        return False
    
# mute someone if the user is admin
def mute(target_username: str):
    with Session(engine) as session:
        target_user = session.get(User, target_username)
        # if the target user is already muted, unmute
        if target_user.is_muted:
            target_user.is_muted = False
        # if the target user is not muted, mute
        else:
            target_user.is_muted = True
        session.commit()

def is_muted(username: str):
    with Session(engine) as session:
        target_user = session.get(User, username)
        # if the target user is already muted, unmute
        if target_user.is_muted:
            return True
        else:
            return False

def is_admin(username: str):
    with Session(engine) as session:
        target_user = session.get(User, username)
        # if the target user is already muted, unmute
        if target_user.is_admin:
            return True
        else:
            return False

# User creates a post
def add_post(username: str, title: str, content: str, category: str):
    with Session(engine) as session:
        time = datetime.datetime.now()
        post = Post(username=username, title=title, content=content, post_category=category, time=time)
        session.add(post)
        session.commit()

# gets posts
def get_posts():
    with Session(engine) as session:
        return session.query(Post).all()

# gets posts by category
def get_category_posts(category: str):
    with Session(engine) as session:
        return session.query(Post).filter(Post.post_category == category).all()

# checks whether the post exists
def post_exists(id: int):
    with Session(engine) as session:
        if session.query(Post).filter(Post.id == id).first() is None:
            return False
        return True
    
# remove post by id
def remove_post(id: int):
    with Session(engine) as session:
        session.query(Post).filter(Post.id == id).delete()
        session.commit()

def get_categories():
    with Session(engine) as session:
        return session.query(Category).all()

def add_category(name: str):
    with Session(engine) as session:
        category = Category(name=name)
        session.add(category)
        session.commit()

def remove_category(name: str):
    with Session(engine) as session:
        session.query(Category).filter(Category.name == name).delete()
        session.commit()

def get_category(name: str):
    with Session(engine) as session:
        return session.get(Category, name)

