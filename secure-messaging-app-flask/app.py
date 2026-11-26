from flask import Flask, render_template, request, abort, url_for, make_response, redirect
from flask_socketio import SocketIO
import db
import secrets
import os
import bcrypt
# import logging

# this turns off Flask Logging, uncomment this to turn off Logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)


app = Flask(__name__)

# secret key used to sign the session cookie
app.config['SECRET_KEY'] = secrets.token_hex()
socketio = SocketIO(app)

# don't remove this!!
import socket_routes

# index page
@app.route("/")
def index():
    return render_template("index.jinja")

# login page
@app.route("/login")
def login():    
    return render_template("login.jinja")

# handles a post request when the user clicks the log in button
@app.route("/login/user", methods=["POST"])
def login_user():
    if not request.is_json:
        abort(404)

    username = request.json.get("username")
    password = request.json.get("password")

    user =  db.get_user(username)
    if user is None:
        return "Error: User does not exist!"

    # check if the hash matches for the password
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return "Error: Password does not match!"

    # successful login
    db.login(username)
    
    # set the cookies and redirect to the friends page
    response = make_response(url_for("friends", username=username))
    response.set_cookie("username", username)

    return response

# handles a get request to the signup page
@app.route("/signup")
def signup():
    return render_template("signup.jinja")

# handles a post request when the user clicks the signup button
@app.route("/signup/user", methods=["POST"])
def signup_user():
    if not request.is_json:
        abort(404)
    username = request.json.get("username")
    password = request.json.get("password")
    
    
    # hash the password
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode('utf-8'), bytes(salt)).decode('utf-8')

    if db.get_user(username) is None:
        db.insert_user(username, password)
        db.login(username)
        # TODO: is it when the username is admin we set the user as admin? or is there any other condition
        if username == "admin":
            db.set_admin(username)
        response = make_response(url_for("friends", username=username))
        response.set_cookie("username", username)
        return response
    return "Error: Username already exists! Please choose a different username."

@app.route("/logout")
def logout():
    db.logout(request.cookies.get("username"))
    return render_template("logout.jinja")

@app.route("/logout/user", methods=["POST"])
def logout_user():
    # after logout, delete the cookies and redirect to the login page
    db.logout(request.cookies.get("username"))
    response = make_response(redirect(url_for("index")))
    response.set_cookie("username", "", expires=0)
    response.set_cookie("room_id", "", expires=0)
    return response

@app.route("/add_friend")
def add_friend():
    username = request.cookies.get("username")
    admin_status = db.is_admin(username)
    return render_template("add_friend.jinja", username=username, is_admin=admin_status)

@app.route("/add_friend/user", methods=["POST"])
def add_friend_user():
    if not request.is_json:
        abort(404)
    username = request.cookies.get("username")
    friend = request.json.get("friend_username")

    if friend.strip() == "":
        return "Error: Invalid empty username!"
    
    if db.get_user(friend) is None:
        return "Error: Friend does not exist!"
    
    if username == friend:
        return "Error: You cannot add yourself as a friend!"
    
    if friend in [user.friend_username for user in db.get_friends(username)]:
        return "Error: Already friends!"
    
    db.insert_friend(username, friend)
    response = make_response(url_for("add_friend", username=username))
    response.set_cookie("username", username)
    return response

@app.route("/friends")
def friends():
    username = request.cookies.get("username")

    # initialise the friend list
    for i in ["admin", "friend1", "Fiona", "Ben"]:
        if username == i:
            continue
        else:
            db.insert_friend(username, i)

    friends = db.get_friends(username)
    admin_status = db.is_admin(username)
    return render_template("friends.jinja", username=username, friends=friends, is_admin=admin_status)

@app.route("/mute")
def mute():
    if request.cookies.get("username") is None:
        abort(404)
    username = request.cookies.get("username")
    if db.is_admin(username):
        users = db.get_all_users()
        admin_status = db.is_admin(username)
        return render_template("mute.jinja", username=username, all_users=users, is_admin=admin_status)
    else:
        abort(403) # forbidden access for non-admin users

# handles a post request when the admin clicks the submit button
@app.route("/mute/user", methods=["POST"])
def mute_user():
    if not request.is_json:
        abort(404)
    username = request.cookies.get("username")
    target_username = request.json.get("target_username")
    users = db.get_all_users()
    # check if the user is admin
    if not db.is_admin(username):
        abort(403) # forbidden access for non-admin users
    # check if the target user exists
    if db.get_user(target_username) is None or target_username not in [user.username for user in users]:
        return "Error: The user you want to mute/unmute does not exist!"
    # check if the target user is admin
    if db.is_admin(target_username):
        return "Error: You cannot mute admin!"
    else:
        # mute/unmute the user
        db.mute(target_username)
        response = make_response(url_for("mute", username=username))
        response.set_cookie("username", username)
        return response

# discussion board page
@app.route("/discussion")
def discussion():
    posts = db.get_posts()
    categories = db.get_categories()
    username = request.cookies.get("username")
    admin_status = db.is_admin(username)
    return render_template("discussion.jinja", posts=posts, categories=categories, username=username, is_admin=admin_status)

# page to add new post
@app.route("/new_post")
def new_post():
    username = request.cookies.get("username")
    categories = db.get_categories()
    if db.is_muted(username):
        return "Error: You are currently muted."
    else:
        return render_template("new_post.jinja", username=username, categories=categories)

@app.route("/categories")
def categories():
    username = request.cookies.get("username")
    categories = db.get_categories()
    admin_status = db.is_admin(username)
    if not db.is_admin(username):
        return "Error: You are not an admin."
    else:
        return render_template("categories.jinja", username=username, categories=categories, is_admin=admin_status)


@app.route("/categories/add", methods=["POST"])
def add_category():
    if not request.is_json:
        abort(404)
    username = request.cookies.get("username")
    category = request.json.get("target_category")
    categories = db.get_categories()
    # check if the user is admin
    if not db.is_admin(username):
        abort(403) # forbidden access for non-admin users
    elif db.get_category(category) is not None:
        return "Error: The category you want to add already exists!"
    else:
        db.add_category(category)
        response = make_response(url_for("categories", username=username, categories=categories))
        response.set_cookie("username", username)
        return response

@app.route("/categories/delete", methods=["POST"])
def delete_category():
    if not request.is_json:
        abort(404)
    username = request.cookies.get("username")
    category = request.json.get("target_category")
    categories = db.get_categories()
    # check if the user is admin
    if not db.is_admin(username):
        abort(403) # forbidden access for non-admin users
    # check if the target user exists
    elif db.get_category(category) is None:
        return "Error: The category you want to delete does not exist!"
    else:
        db.remove_category(category)
        categories = db.get_categories()
        response = make_response(url_for("categories", username=username, categories=categories))
        response.set_cookie("username", username)
        return response

# handler when a "404" error happens
@app.errorhandler(404)
def page_not_found(_):
    return render_template('404.jinja'), 404

# home page, where the messaging app is
@app.route("/message/<friend_username>")
def message(friend_username):
    username = request.cookies.get("username")
    if username is None or friend_username is None:
        abort(404)
    admin_status = db.is_admin(username)
    return render_template("message.jinja", username=username, friend_username=friend_username, is_admin=admin_status)

@app.route("/new_post/user", methods=["POST"])
def new_post_user():
    if not request.is_json:
        abort(404)
    username = request.json.get("username")
    title = request.json.get("title")
    category = request.json.get("category")
    content = request.json.get("content")
    if category is None:
        return "Error: Please select a category!"
    if db.get_user(username) is not None:
        db.add_post(username, title, content, category)
        response = make_response(url_for("discussion", username=username))
        response.set_cookie("username", username)
        return response

@app.route("/remove_post")
def remove_post():
    if request.cookies.get("username") is None:
        abort(404)
    username = request.cookies.get("username")
    if db.is_admin(username):
        posts = db.get_posts()
        admin_status = db.is_admin(username)
        return render_template("remove_post.jinja", username=username, posts=posts, is_admin=admin_status)
    else:
        abort(403)

@app.route("/remove_post/user", methods=["POST"])
def remove_post_user():
    if not request.is_json:
        abort(404)
    username = request.cookies.get("username")
    post_id = request.json.get("target_id")
    posts = db.get_posts()
    if not db.is_admin(username):
        abort(403)
    elif post_id is None:
        return "Error: Please select a post!"
    else:
        try:
            post_id = int(post_id)
            if post_id <= 0:
                return "Error: Invalid post id!"
            elif not db.post_exists(post_id):
                return "Error: The post you want to delete does not exist!"
            else:
                db.remove_post(post_id)
                posts = db.get_posts()
                response = make_response(url_for("remove_post", username=username, posts=posts))
                response.set_cookie("username", username)
                return response
        except ValueError:
            return "Error: Please enter post id as an integer!"
    
if __name__ == '__main__':
    working_directory = os.getcwd()
    certificate_filepath = os.path.join(working_directory, 'certs/server.crt')
    private_key_filepath = os.path.join(working_directory, 'certs/server.key')

    ssl_args = {
        'certfile': certificate_filepath,
        'keyfile': private_key_filepath
    }

    socketio.run(app, host='127.0.0.1', port=8081, **ssl_args)