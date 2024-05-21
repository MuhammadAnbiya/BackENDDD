from models import generate_token
from flask import Flask, json, url_for
from flask_mail import Mail, Message 
from flask import current_app

import secrets
import re
# import requests


# def isHuman(captcha_response):
#     secret = '6LeuVeEpAAAAAK47JTBoE30STSljXm1k46vlGXi4'
#     payload = {'response': captcha_response, 'secret': secret}
#     response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
#     response_text = json.loads(response.text)
#     return response_text['success']

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def is_valid_password(password):
    return len(password) >= 8

def send_password_reset_email(user):
    token = generate_token(user)
    msg = Message('Reset Password Request',
                sender='noreply@example.com',
                recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    Mail.send(msg)
