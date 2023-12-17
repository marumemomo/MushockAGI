import os
from github import Auth, GithubIntegration
import dotenv

def load_github_config():
    dotenv.load_dotenv()
    app_id = os.getenv("GITHUB_APP_ID")
    with open(os.getenv("GITHUB_APP_PRIVATE_KEY"), "r") as f:
        private_key = f.read()
    auth = Auth.AppAuth(app_id=app_id, private_key=private_key)
    gi = GithubIntegration(auth=auth)
    installation = gi.get_installations()[0]
    return installation.get_github_for_installation()

def get_repo_issues(repo):
    return [issue for issue in repo.get_issues(state='open')]
