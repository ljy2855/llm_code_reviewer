import os
import requests

GITHUB_API_URL = "https://api.github.com"
TOKEN_SERVER_URL = "https://github-token-server.vercel.app/api/generate-access-token"


def get_access_token():
    installation_id = get_installation_id()
    access_token = request_access_token_from_server(installation_id)
    return access_token


def get_installation_id():
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    REPO_OWNER = os.getenv("GITHUB_OWNER")
    REPO_NAME = os.getenv("GITHUB_REPOSITORY")
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(
        f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/installation", headers=headers
    )

    if response.status_code == 200:
        installation_id = response.json()["id"]
        return installation_id
    else:
        raise Exception(
            f"Error getting installation_id: {response.status_code} - {response.text}"
        )


def request_access_token_from_server(installation_id):
    headers = {"Content-Type": "application/json"}
    payload = {"installationId": installation_id}

    response = requests.post(TOKEN_SERVER_URL, json=payload, headers=headers)

    if response.status_code == 200:
        access_token = response.json()["token"]
        return access_token
    else:
        raise Exception(
            f"Error getting access token from server: {response.status_code} - {response.text}"
        )
