from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, Response
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            company = user.company
            empresa = company.replace(" ", "-")
            reclame = ReclameAqui(empresa)
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        company = request.form.get('company')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email já existe.', category='error')
        elif len(email) < 4:
            flash('Email deve ser maior que 3 caracteres.', category='error')
        elif len(first_name) < 2:
            flash('O usuário deve ter mais de 1 caratere.', category='error')
        elif password1 != password2:
            flash('Senhas diferentes.', category='error')
        elif len(password1) < 7:
            flash('A senha deve ter mais de 7 caracteres.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'), company = company)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Conta criada!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/saiba-mais', methods=['GET', 'POST'])
def saiba_mais():
    
    return render_template("saiba_mais.html", user=current_user)

@auth.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    
    return render_template("recuperar_senha.html", user=current_user)

@auth.route('/termos', methods=['GET', 'POST'])
def termos():
    
    return render_template("termos.html", user=current_user)

