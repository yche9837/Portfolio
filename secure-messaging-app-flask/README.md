# Secure Messaging App

*INFO2222, University of Sydney*

A web messaging app built with Flask and Socket.IO, focused on secure account handling.

## Features
- Sign-up and login with **bcrypt-hashed passwords**
- Real-time messaging over WebSockets (Socket.IO)
- Served over **HTTPS** (TLS) in local development
- Friend lists, discussion categories and posts
- Admin roles: admins can mute users and remove posts

## Tools
Python · Flask · Flask-SocketIO · SQLAlchemy · SQLite · Jinja

## Run locally
```bash
pip install -r requirements.txt
python3 app.py
```
The app expects a local TLS certificate and key in `certs/`. They are not included in the repository; generate a self-signed pair for local testing.

Because the app uses cookies, test messaging between users in **separate browsers**, not separate tabs.
