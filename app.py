from flask import Flask, render_template, request
from flask_lambda import FlaskLambda
import os
import subprocess
import shutil

app = FlaskLambda(__name__)

def run_command(command):
    """Runs a shell command and returns the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    if request.method == 'POST':
        repo_url = request.form.get('repo_url')
        main_script = request.form.get('main_script')
        repo_dir = "temp_repo"

        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)

        output += f"Cloning repository {repo_url}...\n"
        clone_result = run_command(f"git clone {repo_url} {repo_dir}")
        output += clone_result

        requirements_path = os.path.join(repo_dir, "requirements.txt")
        if os.path.exists(requirements_path):
            output += "\nInstalling requirements...\n"
            install_result = run_command(f"pip install -r {requirements_path}")
            output += install_result

        script_path = os.path.join(repo_dir, main_script)
        if os.path.exists(script_path):
            output += f"\nRunning script {main_script}...\n"
            script_result = run_command(f"python {script_path}")
            output += script_result
        else:
            output += f"\nError: Script {main_script} not found in the repository."

        shutil.rmtree(repo_dir)

    return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
