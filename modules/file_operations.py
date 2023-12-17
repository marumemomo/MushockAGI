import subprocess
import os
from config_loader import load_config

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def run_git_commands(commands):
    for command in commands:
        cwd = os.getcwd()  # Get current working directory
        root_dir = load_config()['root_directory']  # Load project root directory from config
        if cwd != root_dir:
            os.chdir(root_dir)  # Change to the project root directory
        subprocess.run(command)