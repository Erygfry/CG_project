from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Импортируем другие модули
import auth
import deploy

app.register_blueprint(auth.bp)
app.register_blueprint(deploy.bp)

@login_manager.user_loader
def load_user(user_id):
    return auth.User.get(user_id)

@app.route('/')
@login_required
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
