from flask import request, session, flash, redirect, url_for, render_template
from app import app, db, mail
from models import DataUser
from utils import is_valid_email, is_valid_password, send_verification_email
from flask_mail import Message
from werkzeug.security import generate_password_hash

import datetime
import random
import string
import uuid

# Function to generate random token
def generate_token(length=32):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

@app.route("/reset_password_request/", methods=["GET", "POST"])
def reset_password_request():
    if request.method == "POST":
        email = request.form["email-reset"]
        user = DataUser.query.filter_by(email=email).first()
        if user:
            token = str(uuid.uuid4())
            user.reset_token = token
            user.token_expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            db.session.commit()

            send_verification_email(email, token)
            flash('Check your email for the instructions to reset your password', 'info')
            return redirect(url_for('login'))
        else:
            flash('Email address not found', 'danger')
    return render_template('reset_password_request.html')

@app.route("/reset_password/<token>/", methods=['GET', 'POST'])
def reset_password(token):
    user = DataUser.query.filter_by(reset_token=token).first()
    if not user or user.token_expiration < datetime.datetime.utcnow():
        flash('The reset link is invalid or has expired', 'danger')
        return redirect(url_for('reset_password_request'))

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        if is_valid_password(new_password):
            user.password = generate_password_hash(new_password)
            user.reset_token = None
            user.token_expiration = None
            db.session.commit()
            flash('Your password has been reset successfully', 'success')
            return redirect(url_for('login'))
        else:
            flash('Password must be at least 8 characters long', 'danger')
            

@app.route("/dashboard/", methods=['GET'])
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template("dashboard.html", name=username)
    else:
        flash('You are not logged in.', 'danger')
        return redirect(url_for('login'))

@app.route("/login/", methods=['GET', 'POST'])
def login():
    # sitekey = '6LeuVeEpAAAAADWKQuUu6zwZ0BaKlGpFCsws8u_M'  
    if request.method == 'POST':
        email = request.form['email-login']
        password = request.form['password-login']

        user = DataUser.query.filter_by(email=email).first()
        if user and password:
            session['logged_in'] = True
            session['username'] = user.name
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))
    
    return render_template("login.html",)# sitekey=sitekey)


@app.route("/registrasi/", methods=['GET', 'POST'])
def registrasi():
    if request.method == 'POST':
        name = request.form['name-registrasi']
        email = request.form['email-registrasi']
        password = request.form['password-registrasi']
        
        if not name or not email or not password:
            flash('Semua kolom harus diisi.', 'danger')
            return redirect(url_for('registrasi'))

        if not is_valid_email(email):
            flash('Email tidak valid.', 'danger')
            return redirect(url_for('registrasi'))

        if not is_valid_password(password):
            flash('Password harus memiliki minimal 8 karakter.', 'danger')
            return redirect(url_for('registrasi'))

        existing_user = DataUser.query.filter_by(email=email).first()
        if existing_user:
            flash('Email sudah terdaftar.', 'danger')
            return redirect(url_for('registrasi'))
        
        existing_username = DataUser.query.filter_by(name=name).first()
        if existing_username:
            flash('Username sudah terdaftar.', 'danger')
            return redirect(url_for('registrasi'))

        new_registration = DataUser(name=name, email=email, password=password)
        new_registration.save()

        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('login'))

    return render_template("registrasi.html")

@app.route("/logout/", methods=['POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))
