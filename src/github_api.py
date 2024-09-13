import os
import requests


# PR에서 변경된 파일 정보 가져오기
def get_changed_files():
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
    GITHUB_PR_NUMBER = os.getenv("PR_NUMBER")
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls/{GITHUB_PR_NUMBER}/files"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


# PR에 포함된 커밋 리스트 가져오기
def get_pr_commits():
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
    GITHUB_PR_NUMBER = os.getenv("PR_NUMBER")
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls/{GITHUB_PR_NUMBER}/commits"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


# GitHub에 종합적인 리뷰 코멘트 추가
def post_review_comment(commit_id, body):
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
    GITHUB_PR_NUMBER = os.getenv("PR_NUMBER")
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls/{GITHUB_PR_NUMBER}/reviews"

    data = {
        "commit_id": commit_id,
        "body": body,
        "event": "COMMENT",
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    print(f"Posted review comment with status code: {response.status_code}")
