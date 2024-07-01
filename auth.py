from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
import requests

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

class User(UserMixin):
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get(user_id):
        return User(user_id)

@bp.route('/signin/credentials', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Проводим проверку пользователя (замените на свою логику)
        if username == 'test' and password == 'password':
            user = User(username)
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
