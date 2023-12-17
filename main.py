import os
import tomllib
from modules.github_module import load_github_config, get_repo_issues
from modules.llm_module import invoke_llm
from modules.file_operations import read_file, write_file, run_git_commands
from modules.config_loader import load_config
from langchain.llms.ollama import Ollama

g = load_github_config()
config = load_config()
model = config['model']
llm = Ollama(model=model)

repo_name = config['repository']
if not repo_name:
    raise ValueError("Repository name is not set in the config file.")

project_root = config['project_root']

repo = g.get_repo(repo_name)

github_issue_list = []
for issue in get_repo_issues(repo):
    toml_data = tomllib.loads(issue.body)
    file_path = os.path.join(project_root, toml_data['file_path'])
    github_issue_list.append({
        'number': issue.number,
        'description': toml_data["description"],
        'file_path': file_path,
        'branch_name': f"issue-{issue.number}"
    })

for task in github_issue_list:
    run_git_commands([["git", "checkout", "-b", task['branch_name']]])
    code = read_file(task['file_path'])
    task['code'] = code
    changed_code = invoke_llm(llm, task)
    write_file(task['file_path'], changed_code)
    run_git_commands([
        ["git", "add", task['file_path']],
        ["git", "commit", "-m", f"Automated update for issue #{task['number']}"],
        ["git", "push", "-u", "origin", task['branch_name']]
    ])
    pr = repo.create_pull(
        title=f'Automated update for issue #{task['number']}',
        body=f"Fix #{task['number']}",
        head=task['branch_name'],
        base='main'
    )
    run_git_commands([['say', f'"Pull request created: #{pr.number}"']])
