import subprocess
from .config_loader import load_config

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def run_git_commands(commands):
    for command in commands:
        root_dir = load_config()['project_root']
        subprocess.run(command, cwd=root_dir)
