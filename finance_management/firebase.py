import firebase_admin
from firebase_admin import credentials, messaging


cred = credentials.Certificate("finance-management.json")
firebase_admin.initialize_app(cred)


def send_notification(token, title, body, data=None):

    notif = messaging.Notification(title=title, body=body)

    message = messaging.Message(notification=notif, data=data or {}, token=token)

    response = messaging.send(message)
    return response
