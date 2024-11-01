from flask import Flask, render_template, request
import os
import subprocess
import shutil

# Specify the correct template folder path
app = Flask(__name__, template_folder='../templates')  # Adjust the path if needed

def run_command(command):
    """Runs a shell command and returns the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    if request.method == 'POST':
        # Get repo URL and main script name from the form
        repo_url = request.form.get('repo_url')
        main_script = request.form.get('main_script')

        # Define a temporary directory for cloning
        repo_dir = "temp_repo"

        # Remove previous repo if it exists
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)

        # Clone the repository
        output += f"Cloning repository {repo_url}...\n"
        clone_result = run_command(f"git clone {repo_url} {repo_dir}")
        output += clone_result

        # Check for requirements.txt and install if it exists
        requirements_path = os.path.join(repo_dir, "requirements.txt")
        if os.path.exists(requirements_path):
            output += "\nInstalling requirements...\n"
            install_result = run_command(f"pip install -r {requirements_path}")
            output += install_result

        # Run the specified main script
        script_path = os.path.join(repo_dir, main_script)
        if os.path.exists(script_path):
            output += f"\nRunning script {main_script}...\n"
            script_result = run_command(f"python {script_path}")
            output += script_result
        else:
            output += f"\nError: Script {main_script} not found in the repository."

        # Clean up by deleting the cloned repository
        shutil.rmtree(repo_dir)

    return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
