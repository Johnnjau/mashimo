from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
from datetime import datetime, timezone
from . import db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User, Technician, CustomerRequest
from flask import request
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint("main", __name__)

"""
@bp.route('/')
@login_required
def index():
    print("Route:", request.url_rule)
    technicians = Technician.query.all()
    return render_template('index.html', technicians=technicians)
"""

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@bp.route('/', methods=['GET', 'POST'])
def index():
    technicians = Technician.query.all()
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        service_needed = request.form.get('service_needed')
        
        if not customer_name or not service_needed:
            flash('Both customer name and service needed are required', 'error')
        else:
            new_request = CustomerRequest(customer_name=customer_name, service_needed=service_needed)
            try:
                db.session.add(new_request)
                db.session.commit()
                flash('Request submitted successfully', 'success')
            except SQLAlchemyError as e:
                db.session.rollback()
                flash('Error submitting request', 'error')
                print(f"Error: {e}")
        
        return redirect(url_for('bp.index'))

    requests = CustomerRequest.query.all()
    return render_template('index.html', technicians=technicians, requests=requests)


@bp.route('/requests')
@login_required
def requests():
    # Replace with your actual data fetching logic
    requests = []
    return render_template('requests.html', title='Customer Requests', requests=requests)
