from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import subprocess
import os
import re

bp = Blueprint('deploy', __name__, url_prefix='/deploy')

GITHUB_URL_REGEX = r'^(https:\/\/|git@)github\.com[/:][\w\-]+\/[\w\-]+(\.git)?$'

@bp.route('/', methods=['GET', 'POST'])
@login_required
def deploy():
    if request.method == 'POST':
        source = request.form.get('source')
        if not source or not re.match(GITHUB_URL_REGEX, source):
            return jsonify(error="Invalid GitHub URL"), 400

        username = current_user.id
        user_dir = f'/var/www/{username}'

        try:
            if os.path.exists(user_dir):
                subprocess.run(['rm', '-rf', f'{user_dir}/.[!.]*', f'{user_dir}/*'], check=True)
            else:
                os.makedirs(user_dir)

            subprocess.run(['git', 'clone', source, user_dir], check=True)
            subprocess.run(['npm', 'install'], cwd=user_dir, check=True)
            subprocess.run(['npm', 'fund'], cwd=user_dir, check=True)
            subprocess.run(['npm', 'run', 'build'], cwd=user_dir, check=True)
            subprocess.run(['pm2', 'start', 'npm', '--name', f'{username}-server', '--', 'start'], cwd=user_dir, check=True)

            return jsonify(message=f"Repository cloned successfully to {user_dir}"), 200
        except subprocess.CalledProcessError as e:
            return jsonify(error=f"Internal Server Error: {e}"), 500

    return render_template('deploy.html')
