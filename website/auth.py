from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user: 
            if check_password_hash(user.password, password):
                flash('Welcome to Recycle Nexus!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
                

    return render_template("login.html", user=current_user )


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
   

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        lastname = request.form.get('lastname')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash('Email address already in use. Please use a different email.', category='error')
            return redirect(url_for('views.sign_up'))

        # Continue with creating the user if email is unique
        if password1 != password2:
            flash('Passwords do not match!', category='error')
            return redirect(url_for('views.sign_up'))
        
        new_user = User(email=email, firstname=firstname, lastname=lastname, password=generate_password_hash(password1, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash('Account created!', category='success')
        login_user(new_user, remember=True)
        return redirect(url_for('views.login'))


    return render_template("sign-up.html", user=current_user)