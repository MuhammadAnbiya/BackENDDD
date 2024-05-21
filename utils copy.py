import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def is_valid_password(password):
    return len(password) >= 8

def send_verification_email(email, token):
    msg = MIMEMultipart()

    sender_email = app.config["MAIL_USERNAME"]
    sender_password = app.config["MAIL_PASSWORD"]
    receiver_email = email

    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Password Reset Request"

    reset_password_url = url_for('reset_password', token=token, _external=True)
    body = f"To reset your password, visit the following link: {reset_password_url}"

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        flash('Check your email for the instructions to reset your password', 'info')
        print("Email verifikasi CAPTCHA telah berhasil dikirim.")
    except Exception as e:
        flash(f"Terjadi kesalahan saat mengirim email: {e}", 'danger')
    finally:
        server.quit()

