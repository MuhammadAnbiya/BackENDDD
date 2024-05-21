import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app import app

import smtplib

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def is_valid_password(password):
    return len(password) >= 8

def send_verification_email(email, captcha_code):
    sender_email = app.config["MAIL_USERNAME"] 
    sender_password = app.config["MAIL_PASSWORD"]      

    receiver_email = email
    msg = MIMEMultipart()

    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Verifikasi CAPTCHA"

    body = f"Kode CAPTCHA Anda adalah: {captcha_code}. Silakan masukkan kode ini untuk verifikasi."

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email verifikasi CAPTCHA telah berhasil dikirim.")
    except Exception as e:
        print(f"Terjadi kesalahan saat mengirim email: {e}")
    finally:
        server.quit()

email = "anbiya17agustus@gmail.com"  
captcha_code = "123456"           
send_verification_email(email, captcha_code)