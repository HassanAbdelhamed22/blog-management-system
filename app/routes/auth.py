from flask import Blueprint, request, render_template, redirect, url_for
from flask_injector import inject
from flask_login import login_user, logout_user, current_user, login_required
from app.forms.loginForm import LoginForm
from app.forms.signupForm import SignupForm
from app.services.sql.user import UserService

auth = Blueprint("auth", __name__)

# User Profile Route (Protected)
@auth.route('/')
@login_required
def profile():
    if not current_user.has_role('user'):
        return redirect(url_for('auth.login_form'))
    return render_template('/auth/profile.html', user=current_user)

# Show Login Form
@auth.route('/login')
def login_form():
    form = LoginForm()
    return render_template("/auth/login.html", form=form)

# Login Route
@auth.route('/login', methods=['POST'])
@inject
def login(user_service: UserService):
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

    if not username or not password:
        return render_template("/auth/login.html", message="Please enter both username and password", form=form)

    status = user_service.login(username=username, password=password)

    if status:
        if current_user.has_role('admin'):
            return redirect(url_for('admin.admin_dashboard'))
        if current_user.has_role('author'):
            return redirect(url_for('author.view_posts'))
        return redirect(url_for('user.view_blogs'))
    else:
        return render_template("/auth/login.html", message="Incorrect username or password", form=form)

# Show Signup Form
@auth.route('/signup')
def signup_form():
    form = SignupForm()
    return render_template("/auth/signup.html", form=form)

# Handle Signup (POST)
@auth.route('/signup', methods=['POST'])
@inject
def signup(user_service: UserService):
    form = SignupForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

    if not username or not email or not password:
        return render_template("/auth/signup.html", message="All fields are required", form=form)
    
    if user_service.username_exists(username):
        return render_template("/auth/signup.html", message="Username already exists", form=form)

    if user_service.email_exists(email):
        return render_template("/auth/signup.html", message="Email already exists", form=form)


    user = user_service.register(username=username, email=email, password=password)

    if user:
        return redirect(url_for('auth.login_form'))
    else:
        return render_template("/auth/signup.html", message="Registration failed", form=form)

# Logout Route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login_form'))
