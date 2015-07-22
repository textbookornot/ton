from flask import render_template, redirect, url_for, flash, jsonify, request
from flask.ext.login import login_user, logout_user, login_required, current_user

from . import app, db
from .forms import RegisterForm, LoginForm

from .models import User


@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/index')
def angular_index():
    return render_template('angular_index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    # if post is sent we attempt to log them in
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.is_correct_password(form.password.data):
            login_user(user)
            flash('logged in')
            return redirect(url_for('index'))
        else:
            flash('incorrect email or password')
            return redirect(url_for('login'))
    else:
        errors = {field: error.pop() for field, error in form.errors.items()}
        for error in errors.values(): flash(error)

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated():
        logout_user()
        flash('logged out')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    # if post is sent we sign them up
    if request.method == 'POST' and form.validate():
        user = User(
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash('thanks for registering')
        return redirect(url_for('index'))
    else:
        errors = {field: error.pop() for field, error in form.errors.items()}
        for error in errors.values(): flash(error)

    return render_template('register.html', form=form)


@app.route('/api/login', methods=['POST'])
def api_login():
    json_data = request.json
    user = User.query.filter_by(email=json_data['email']).first()
    if user and user.is_correct_password(json_data['password']):
        login_user(user)
        json = {
            'success': True,
            'user': {
                'email': current_user.email
            }
        }
    else:
        json = {
            'success': False,
            'errors': 'incorrect email or password'
        }
    return jsonify(json)


@app.route('/api/logout')
def api_logout():
    if current_user.is_authenticated():
        logout_user()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@app.route('/api/register', methods=['POST'])
def api_register():
    form = RegisterForm.from_json(request.json)
    if form.validate():
        user = User(
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        json = {'success': True}
    else:
        errors = {field: error.pop() for field, error in form.errors.items()}
        json = {
            'success': False,
            'errors': errors
        }

    return jsonify(json)
