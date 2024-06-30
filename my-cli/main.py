from pprint import pprint

from constants.env import env
from github import api as github_service

if __name__ == "__main__":
    print(env.get("GITHUB_TOKEN"))

    data = github_service.get_repos_of_auth_user()
    pprint(data)
