import os
import requests
from lxml import etree

USERNAME = os.environ.get("USER_NAME", "arman-haider1")
TOKEN = os.environ.get("ACCESS_TOKEN") or os.environ.get("GITHUB_TOKEN")

HEADERS = {"Accept": "application/vnd.github+json"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

def github_get(path):
    r = requests.get(f"https://api.github.com{path}", headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()

def stats():
    user = github_get(f"/users/{USERNAME}")
    repos = github_get(f"/users/{USERNAME}/repos?per_page=100&type=owner")
    repo_count = user["public_repos"]
    followers = user["followers"]
    following = user["following"]
    stars = sum(repo.get("stargazers_count", 0) for repo in repos)
    return repo_count, stars, followers, following

def replace(root, element_id, value):
    el = root.find(f".//*[@id='{element_id}']")
    if el is not None:
        el.text = str(value)

def update_svg(filename, repo_count, stars, followers):
    tree = etree.parse(filename)
    root = tree.getroot()
    replace(root, "repo_data", repo_count)
    replace(root, "star_data", stars)
    replace(root, "follower_data", followers)
    tree.write(filename, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    repo_count, stars, followers, following = stats()
    update_svg("dark_mode.svg", repo_count, stars, followers)
    update_svg("light_mode.svg", repo_count, stars, followers)
    print(f"Updated {USERNAME}: {repo_count} repos, {stars} stars, {followers} followers, {following} following")
