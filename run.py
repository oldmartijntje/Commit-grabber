import requests
from collections import Counter

# Replace with your GitHub username and token
username = "your_username"
token = "your_token"

headers = {"Authorization": f"token {token}"}
repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"

# Get all public repos
repos = requests.get(repos_url, headers=headers).json()
commit_messages = []

for repo in repos:
    repo_name = repo['name']
    commits_url = f"https://api.github.com/repos/{username}/{repo_name}/commits?author={username}&per_page=100"
    commits = requests.get(commits_url, headers=headers).json()
    for commit in commits:
        try:
            msg = commit['commit']['message']
            commit_messages.append(msg.strip())
        except KeyError:
            continue

# Count and print most common messages
counter = Counter(commit_messages)
most_common = counter.most_common(10)
print("\nTop 10 most common commit messages:")
for msg, count in most_common:
    print(f"{msg} — {count} times")
