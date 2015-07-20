from flask import render_template, redirect, url_for, flash
from flask.ext.login import login_user, logout_user, login_required

from . import app, db
from .forms import EmailPasswordForm, LoginForm

from .models import User

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    # if post is sent we attempt to log them in
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user.is_correct_password(form.password.data):
            login_user(user)
            flash('Logged in')

            # next = flask.request.args.get('next')
            # if not next_is_valid(next):
                # return flask.abort(400)

            return redirect(url_for('index'))
        else:
            flash('Wrong password')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('index'))


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = EmailPasswordForm()

    # if post is sent we sign them up
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('index'))

    return render_template('login.html', form=form)
