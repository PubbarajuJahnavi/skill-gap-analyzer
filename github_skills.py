import requests

def get_github_skills(username):
    """Fetch programming languages used across a GitHub user's public repos."""
    if not username or username.strip() == "":
        return set()

    url = f"https://api.github.com/users/{username.strip()}/repos"
    response = requests.get(url)

    if response.status_code != 200:
        return set()

    repos = response.json()
    if not isinstance(repos, list):
        return set()

    languages = set()
    for repo in repos:
        lang_url = repo.get("languages_url")
        if not lang_url:
            continue
        lang_response = requests.get(lang_url)
        if lang_response.status_code == 200:
            langs = lang_response.json()
            languages.update([lang.lower() for lang in langs.keys()])

    return languages