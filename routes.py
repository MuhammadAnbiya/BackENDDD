from flask import request, session, flash, redirect, url_for, render_template
from app import app, db, bcrypt
from models import DataUser
from utils import is_valid_email, is_valid_password

@app.route("/dashboard/")
def dashboard():
    if 'logged_in' in session:
        user_id = session.get('user_id')
        user = DataUser.query.get(user_id)
        if user:
            return render_template("dashboard.html", name=user.name)
        else:
            flash('User not found.', 'danger')
            return redirect(url_for('login'))
    else:
        flash('You are not logged in.', 'danger')
        return redirect(url_for('login'))

@app.route("/registrasi/", methods=['GET', 'POST'])
def registrasi():
    if request.method == 'POST':
        name = request.form['name-registrasi']
        email = request.form['email-registrasi']
        password = request.form['password-registrasi']
        confirm_password = request.form['confirm-password-registrasi']  # Tambahkan ini
        
        if not name or not email or not password or not confirm_password: 
            flash('Semua kolom harus diisi.', 'danger')
            return redirect(url_for('registrasi'))

        if not is_valid_email(email):
            flash('Email tidak valid.', 'danger')
            return redirect(url_for('registrasi'))

        if not is_valid_password(password):
            flash('Password harus memiliki minimal 8 karakter.', 'danger')
            return redirect(url_for('registrasi'))
        
        if password != confirm_password:  
            flash('Konfirmasi password tidak sesuai.', 'danger')
            return redirect(url_for('registrasi'))

        existing_user = DataUser.query.filter_by(email=email).first()
        if existing_user:
            flash('Email sudah terdaftar.', 'danger')
            return redirect(url_for('registrasi'))

        new_registration = DataUser(name=name, email=email, password=password)
        new_registration.save()

        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('login'))

    return render_template("registrasi.html")


@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email-login']
        password = request.form['password-login']

        user = DataUser.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['logged_in'] = True
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login'))
    
    return render_template("login.html")

@app.route("/logout/", methods=['POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))