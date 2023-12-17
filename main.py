import yaml
import re
from langchain.llms.ollama import Ollama
from github import Auth, GithubIntegration
import tomllib
import dotenv
import os
import subprocess

dotenv.load_dotenv()
app_id = os.getenv("GITHUB_APP_ID")
with open(os.getenv("GITHUB_APP_PRIVATE_KEY"), "r") as f:
    private_key = f.read()
auth = Auth.AppAuth(
    app_id=app_id,
    private_key=private_key,
)
gi = GithubIntegration(auth=auth)
installation = gi.get_installations()[0]
g = installation.get_github_for_installation()
repo = g.get_repo("marumemomo/MushockAGI")

github_issue_list = []

for issue in repo.get_issues(state='open'):
    toml_data = tomllib.loads(issue.body)
    print(toml_data)
    github_issue_list.append({
        'number': issue.number,
        'description': toml_data["description"],
        'file_path': toml_data['file_path'],
        'branch_name': f"issue-{issue.number}"
    })

with open('config.yml', 'r') as stream:
    config = yaml.safe_load(stream)

model = config['model']
llm = Ollama(
    model=model
)

for task in github_issue_list:
    subprocess.run(["git", "checkout", "-b", task['branch_name']])
    with open(task['file_path'], 'r') as code_file:
        code = code_file.read()
    print("[Invoke LLM]")
    response =  llm.invoke(
    f"""
    You are a Professional Python programmer.
    Please change the following code with the following description.
    The changed code should be output using code blocks.
    Be sure to output all code for final export to a file.

    Description:
    {task['description']}

    Code:
    {code}
    """)

    # Extracting code block from response
    matches = re.findall(r'```.*\n\s*([\s\S]*?)\n```', response, re.MULTILINE)
    if len(matches) > 0:
        changed_code = matches[0]
    else:
        print("No code block found in the response.")
        changed_code = response
    print("[Code Result]")
    print(changed_code)

    # Write the modified code to the file
    with open(task['file_path'], 'w') as code_file:
        code_file.write(changed_code)

    # Commit and push the changes to the new branch
    subprocess.run(["git", "add", task['file_path']])
    subprocess.run(["git", "commit", "-m", f"Automated update for issue #{task['number']}"])
    subprocess.run(["git", "push", "-u", "origin", task['branch_name']])

    # Create a pull request
    pr = repo.create_pull(
        title=f'Automated update for issue #{task['number']}',
        body=f'Fix #{task['number']}',
        head=task['branch_name'],
        base='main'
    )

    print(f'Pull request created: #{pr.number}')

# Run macOS say command at the end of program execution
subprocess.run(['/usr/bin/osascript', '-e', 'display dialog "Process completed successfully." buttons {"OK"} default button 1'])