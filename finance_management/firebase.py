import firebase_admin
from firebase_admin import credentials, messaging
from dotenv import load_dotenv
import os

load_dotenv()

FIREBASE_CONFIG_PATH = os.getenv("FIREBASE_PATH")

if not FIREBASE_CONFIG_PATH is None:

    cred = credentials.Certificate(FIREBASE_CONFIG_PATH)
    firebase_admin.initialize_app(cred)


def send_notification(token, title, body, data=None):

    notif = messaging.Notification(title=title, body=body)

    message = messaging.Message(notification=notif, data=data or {}, token=token)

    response = messaging.send(message)
    return response
