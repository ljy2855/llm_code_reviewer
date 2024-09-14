import os
import requests


# PR에서 변경된 파일 정보 가져오기
def get_changed_files(installation_token):
    GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
    GITHUB_PR_NUMBER = os.getenv("PR_NUMBER")

    # Authorization 헤더에 installation_token을 사용
    headers = {
        "Authorization": f"Bearer {installation_token}",
        "Accept": "application/vnd.github+json",
    }

    # PR의 파일 변경 사항을 가져오는 GitHub API 요청 URL
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls/{GITHUB_PR_NUMBER}/files"

    # API 요청
    response = requests.get(url, headers=headers)

    # 요청 실패 시 예외 발생
    response.raise_for_status()

    # 응답 결과 반환
    return response.json()


# PR에 포함된 커밋 리스트 가져오기
def get_pr_commits(installation_token):
    GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
    GITHUB_PR_NUMBER = os.getenv("PR_NUMBER")

    headers = {
        "Authorization": f"Bearer {installation_token}",
        "Accept": "application/vnd.github+json",
    }

    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls/{GITHUB_PR_NUMBER}/commits"
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 오류 발생 시 예외 처리
    return response.json()  # 커밋 리스트 반환


# GitHub에 종합적인 리뷰 코멘트 추가
def post_review_comment(commit_id, body, github_token):
    GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
    GITHUB_PR_NUMBER = os.getenv("PR_NUMBER")

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json",
    }

    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls/{GITHUB_PR_NUMBER}/reviews"

    data = {
        "commit_id": commit_id,
        "body": body,
        "event": "COMMENT",
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()  # 오류 발생 시 예외 처리
    print(f"Posted review comment with status code: {response.status_code}")
