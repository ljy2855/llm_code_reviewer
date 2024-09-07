import os
import requests
import json

# GitHub 환경 변수에서 액세스 토큰과 PR 정보 가져오기
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
GITHUB_PR_NUMBER = os.getenv("GITHUB_PR_NUMBER")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
PROMT = os.getenv("PROMT")
# GitHub API의 헤더 설정
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


# PR에서 변경된 파일 정보 가져오기
def get_changed_files():
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls/{GITHUB_PR_NUMBER}/files"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


# PR에 포함된 커밋 리스트 가져오기
def get_pr_commits():
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls/{GITHUB_PR_NUMBER}/commits"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


# Ollama API로 코드 리뷰 요청
def get_ollama_review(code_diff):
    ollama_url = os.getenv("OLLAMA_API_URL")
    headers = {"Content-Type": "application/json"}
    data = {
        "model": OLLAMA_MODEL,
        "prompt": f"{PROMT}\n{code_diff}",
        "stream": False,
    }

    response = requests.post(f"{ollama_url}/api/generate", json=data, headers=headers)
    print(f"Ollama API response: {response.text}")
    if response.status_code == 200:
        result = response.text
        result = json.loads(result)
        print(f"Ollama API response: {result}")
        return result.get("response", "")
    else:
        return "Ollama API 호출 실패"


# 코드 리뷰 요청 (GitHub API로 PR에 종합적인 코멘트 추가)
def post_review_comment(commit_id, body):

    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls/{GITHUB_PR_NUMBER}/reviews"

    data = {
        "commit_id": commit_id,
        "body": body,  # 전체적인 리뷰 코멘트
        "event": "COMMENT",  # "COMMENT" 이벤트를 사용하여 인라인 코멘트 없이 종합적인 리뷰 남김
    }

    response = requests.post(url, json=data, headers=headers)
    print(f"Response status code: {response.status_code}")
    print(f"Response body: {response.text}")

    response.raise_for_status()


def main():
    # PR에서 변경된 파일 정보 가져오기
    changed_files = get_changed_files()

    # PR에서 커밋 리스트 가져오기
    commits = get_pr_commits()

    # 첫 번째 커밋을 사용 (다른 로직으로 원하는 커밋을 선택할 수 있습니다)
    if commits:
        commit_id = commits[0]["sha"]
    else:
        print("No commits found in the pull request.")
        return

    # 모든 변경 파일의 diff를 하나의 문자열로 결합
    code_diff = "\n".join([file["patch"] for file in changed_files if "patch" in file])

    if code_diff:
        # Ollama API에 코드 리뷰 요청
        review_comment = get_ollama_review(code_diff)

        # PR에 종합적인 코멘트 남기기
        post_review_comment(commit_id, review_comment)
    else:
        print("코드 변경 사항이 없습니다.")


if __name__ == "__main__":
    main()
