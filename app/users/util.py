import os
import uuid
from flask_mail import Message
from flask import url_for
from PIL import Image
from app import mail
from flask import current_app

def send_request_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
    sender = 'sally_xu@hotmail.com', 
    recipients=[user.email])
    msg.body = "To reset your password, visit the following link: {} \nif you did not make this request then simply ignore this email, and no changes will be made.".format(url_for('users.reset_password', token=token, _external=True))
    mail.send(msg)

def save_picture(form_picture):
    random_hex = uuid.uuid4().hex
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn