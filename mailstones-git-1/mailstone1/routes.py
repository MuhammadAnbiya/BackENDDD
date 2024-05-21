from flask import request, session, flash, redirect, url_for, render_template
from app import app
from models import DataUser
from utils import is_valid_email, is_valid_password

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
    if request.method == 'POST':
        name = request.form['name-login']
        password = request.form['password-login']

        user = DataUser.query.filter_by(name=name).first()
        if user and password:
            session['logged_in'] = True
            session['username'] = user.name
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))
    
    return render_template("login.html")

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
