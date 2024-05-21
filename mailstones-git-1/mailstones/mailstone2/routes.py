from flask import request, session, flash, redirect, url_for, render_template
from models import DataUser
from utils import is_valid_email, is_valid_password, send_password_reset_email
from flask_mail import Message
from app import app, db
from flask_bcrypt import generate_password_hash


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
    sitekey = '6LeuVeEpAAAAADWKQuUu6zwZ0BaKlGpFCsws8u_M'

    if request.method == 'POST':
        email = request.form['email-login']
        password = request.form['password-login']
        # captcha_response = request.form['g-recaptcha-response']
        
        # if not isHuman(captcha_response):
        #     flash('reCAPTCHA verification failed. Please try again.', 'danger')
        #     return redirect(url_for('login'))

        user = DataUser.query.filter_by(email=email).first()
        if user and password: #check_password_hash(user.password, password):
            session['logged_in'] = True
            session['username'] = user.name
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login')) 
    return render_template("login.html") #, sitekey=sitekey)
    

@app.route("/reset_password_request", methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form['email']
        user = DataUser.query.filter_by(email=email).first()
        if user:
            send_password_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('login'))
        else:
            flash('Email address not found.', 'danger')
    return render_template('reset_password_request.html')


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    user = DataUser.verify_reset_password_token(token)
    if not user:
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('reset_password_request'))
    if request.method == 'POST':
        user.password = generate_password_hash(request.form['password'])
        db.session.commit()
        flash('Your password has been reset.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html')


@app.route("/registrasi/", methods=['GET', 'POST'])
def registrasi():
    sitekey = '6LeuVeEpAAAAADWKQuUu6zwZ0BaKlGpFCsws8u_M'

    if request.method == 'POST':
        name = request.form['name-registrasi']
        email = request.form['email-registrasi']
        password = request.form['password-registrasi']
        confirm_password = request.form['confirm-password-registrasi']
        # captcha_response = request.form['g-recaptcha-response']

        
        if not name or not email or not password or not confirm_password:
            flash('Semua kolom harus diisi.', 'danger')
            return redirect(url_for('registrasi'))

        if not is_valid_email(email):
            flash('Email tidak valid.', 'danger')
            return redirect(url_for('registrasi'))

        if not is_valid_password(password):
            flash('Password harus memiliki minimal 8 karakter.', 'danger')
            return redirect(url_for('registrasi'))
        
        # if not isHuman(captcha_response):
        #     flash('Verifikasi reCAPTCHA gagal. Silakan coba lagi.', 'danger')
        #     return redirect(url_for('registrasi'))

        if password != confirm_password:
            flash('Password dan konfirmasi password tidak cocok.', 'danger')
            return redirect(url_for('registrasi'))

        existing_user = DataUser.query.filter_by(email=email).first()
        if existing_user:
            flash('Email sudah terdaftar.', 'danger')
            return redirect(url_for('registrasi'))
        
        existing_username = DataUser.query.filter_by(name=name).first()
        if existing_username:
            flash('Username sudah terdaftar.', 'danger')
            return redirect(url_for('registrasi'))

        # hashed_password = generate_password_hash(password)
        new_registration = DataUser(name=name, email=email, password=password)#hashed_password)
        new_registration.save()

        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('login'))

    return render_template("registrasi.html")#, sitekey=sitekey)


@app.route("/logout/", methods=['POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))
