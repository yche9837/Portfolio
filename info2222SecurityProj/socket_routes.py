'''
socket_routes
file containing all the routes related to socket.io
'''


from flask_socketio import join_room, emit, leave_room
from flask import request
import rsa
import db


try:
    from __main__ import socketio
except ImportError:
    from app import socketio

from models import Room

import db

room = Room()

def encrypt(data, key):
    return rsa.encrypt(bytes(data, "utf-8"), key)

def generate_key_pair(username):
    (public, private) = rsa.newkeys(2048)

    with open(f"key/{username}_pk.pem", "wb") as f:
        f.write(public._save_pkcs1_pem())

    with open(f"key/{username}_sk.pem", "wb") as f:
        f.write(private._save_pkcs1_pem())

    return public, private

# TODO: send public key

"""
TODO: encrypt message
"""

"""
TODO: decrypt message
"""

# when the client connects to a socket
# in JS, this is done via the io() function
@socketio.on('connect')
def connect():
    username = request.cookies.get("username")
    room_id = request.cookies.get("room_id")
    if room_id is None or username is None:
        return
    # socket automatically leaves a room on client disconnect
    # so on client connect, the room needs to be rejoined
    join_room(int(room_id))
    emit("incoming", (f"{username} has connected", "green"), to=int(room_id))

# event when client disconnects
# quite unreliable use sparingly
@socketio.on('disconnect')
def disconnect():
    username = request.cookies.get("username")
    room_id = request.cookies.get("room_id")
    if room_id is None or username is None:
        return
    emit("incoming", (f"{username} has disconnected", "red"), to=int(room_id))

# send message event handler
@socketio.on("send")
def send(username, message, room_id):
    key = rsa.PublicKey._load_pkcs1_pem(open(f"key/{username}_pk.pem", "rb").read())
    msg = encrypt(message, key)
    emit("incoming", (f"{username}: {msg}"), to=room_id)

# exchanging public key
@socketio.on("exchange_pk")
def exchange_pk(sender_name, receiver_name):
    # sender's public key
    with open(f"key/{sender_name}_pk.pem", "r") as f:
        sender_public_key_pem = f.read()
    
    # receiver's public key
    with open(f"key/{receiver_name}_pk.pem", "r") as f:
        receiver_public_key_pem = f.read()

    # emit sender's pk to receiver and vice versa
    emit("public_key", {"username": sender_name, "public_key": sender_public_key_pem}, room=receiver_name)
    emit("public_key", {"username": receiver_name, "public_key": receiver_public_key_pem}, room=sender_name)          
    
# join room event handler
@socketio.on("join")
def join(sender_name, receiver_name):
    
    receiver = db.get_user(receiver_name)
    if receiver is None:
        return "Unknown receiver!"
    
    sender = db.get_user(sender_name)
    if sender is None:
        return "Unknown sender!"
    if sender.is_muted:
        return "You are muted! You cannot send messages."

    if db.get_login_status(receiver_name) is False:
        return f"{receiver_name} is not logged in!"

    # both user logged in, generate the user's key pair
    generate_key_pair(username=sender_name)

    room_id = room.get_room_id(receiver_name)

    if room_id is not None:
        
        room.join_room(sender_name, room_id)
        join_room(room_id)
        # emit to everyone in the room except the sender
        emit("incoming", (f"{sender_name} has joined the room.", "green"), to=room_id, include_self=False)
        # emit only to the sender
        emit("incoming", (f"{sender_name} has joined the room. Now talking to {receiver_name}.", "green"))
        return room_id
    
    room_id = room.create_room(sender_name, receiver_name)
    emit("incoming", (f"{sender_name} has joined the room. Now talking to {receiver_name}.", "green"), to=room_id)

    # exchange public keys
    exchange_pk(sender_name, receiver_name)
    
    return room_id

# leave room event handler
@socketio.on("leave")
def leave(username, room_id):
    emit("incoming", (f"{username} has left the room.", "red"), to=room_id)
    leave_room(room_id)
    room.leave_room(username)

