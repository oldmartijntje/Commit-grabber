import requests
import os
import csv

# Function to manually load .env file into environment variables
def load_dotenv_file(env_path):
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.lstrip('\ufeff').strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")
    except FileNotFoundError:
        print(f".env file not found at: {env_path}")

# Load environment variables
dotenv_path = "./.env"
load_dotenv_file(dotenv_path)

username = os.getenv("GH_NAME")
token = os.getenv("API_KEY")

print("GH_NAME =", username)
print("API_KEY startswith ghp_? =>", token[:4] if token else None)

headers = {"Authorization": f"token {token}"} if token else {}
repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"

# Get all public repos
repos_response = requests.get(repos_url, headers=headers)
if repos_response.status_code != 200:
    print(f"Failed to fetch repos: {repos_response.status_code} - {repos_response.text}")
    repos = []
else:
    repos = repos_response.json()

# Prepare rows: list of [repo_name, message, sha, date]
rows = []

for repo in repos:
    repo_name = repo["name"]
    commits_url = (
        f"https://api.github.com/repos/{username}/{repo_name}/commits"
        f"?author={username}&per_page=100"
    )
    commits_response = requests.get(commits_url, headers=headers)
    if commits_response.status_code != 200:
        print(f"Failed to fetch commits for {repo_name}: {commits_response.status_code}")
        continue

    commits = commits_response.json()
    for commit in commits:
        try:
            message = commit["commit"]["message"].strip()
            sha = commit["sha"]
            date = commit["commit"]["author"]["date"]
            rows.append([repo_name, message, sha, date])
        except KeyError:
            continue

# Write to CSV
csv_path = "commit_details.csv"
with open(csv_path, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["repository", "message", "commit_hash", "date"])
    writer.writerows(rows)

print(f"\nExported {len(rows)} commits to '{csv_path}'")
