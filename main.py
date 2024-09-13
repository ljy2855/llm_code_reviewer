import os
import requests
import json


class PromptType:
    GENERAL_REVIEW = "GENERAL_REVIEW"
    SECURITY_REVIEW = "SECURITY_REVIEW"
    FUNCTIONALITY_REVIEW = "FUNCTIONALITY_REVIEW"
    CODE_STYLE_REVIEW = "CODE_STYLE_REVIEW"
    TEST_COVERAGE_REVIEW = "TEST_COVERAGE_REVIEW"


def generate_prompt(prompt_type, pr_title, pr_body, code_diff, prompt_language="EN"):
    if prompt_language == "EN":
        if prompt_type == PromptType.GENERAL_REVIEW:
            return f'The following pull request is titled: "{pr_title}".\nThe pull request description is as follows: "{pr_body}".\nPlease review the code changes made in this pull request:\n\n{code_diff}'

        elif prompt_type == PromptType.SECURITY_REVIEW:
            return f'A pull request has been created with the title "{pr_title}" and the description "{pr_body}".\nPlease review the code with a focus on security aspects. Check for any potential vulnerabilities such as SQL injection, XSS, or improper handling of sensitive data:\n\n{code_diff}'

        elif prompt_type == PromptType.FUNCTIONALITY_REVIEW:
            return f'The pull request is titled: "{pr_title}" and described as: "{pr_body}".\nReview the code specifically to ensure the correct implementation of the requested functionality:\n\n{code_diff}'

        elif prompt_type == PromptType.CODE_STYLE_REVIEW:
            return f'The following pull request with the title "{pr_title}" and description "{pr_body}" has been submitted.\nPlease review the code for adherence to best practices in terms of readability, maintainability, and performance optimization:\n\n{code_diff}'

        elif prompt_type == PromptType.TEST_COVERAGE_REVIEW:
            return f'This pull request, titled "{pr_title}" and described as "{pr_body}", has been submitted.\nPlease review the code for testing coverage. Ensure that the code changes are thoroughly tested and check if the tests cover edge cases:\n\n{code_diff}'

        else:
            return f'Please review this pull request: "{pr_title}".\n{code_diff}'

    elif prompt_language == "KR":
        if prompt_type == PromptType.GENERAL_REVIEW:
            return f'다음 풀 리퀘스트 제목: "{pr_title}".\n풀 리퀘스트 설명: "{pr_body}".\n이 풀 리퀘스트의 코드 변경 사항을 리뷰해 주세요:\n\n{code_diff}'

        elif prompt_type == PromptType.SECURITY_REVIEW:
            return f'제목이 "{pr_title}"이고 설명이 "{pr_body}"인 풀 리퀘스트가 생성되었습니다.\n보안적인 관점에서 코드를 리뷰해 주세요. SQL 인젝션, XSS, 민감한 데이터 처리 등의 취약점이 있는지 확인해 주세요:\n\n{code_diff}'

        elif prompt_type == PromptType.FUNCTIONALITY_REVIEW:
            return f'풀 리퀘스트 제목: "{pr_title}", 설명: "{pr_body}".\n요청된 기능이 올바르게 구현되었는지 리뷰해 주세요:\n\n{code_diff}'

        elif prompt_type == PromptType.CODE_STYLE_REVIEW:
            return f'제목이 "{pr_title}"이고 설명이 "{pr_body}"인 풀 리퀘스트가 제출되었습니다.\n코드의 가독성, 유지보수성, 성능 최적화 측면에서 리뷰해 주세요:\n\n{code_diff}'

        elif prompt_type == PromptType.TEST_COVERAGE_REVIEW:
            return f'제목이 "{pr_title}"이고 설명이 "{pr_body}"인 풀 리퀘스트가 제출되었습니다.\n테스트 커버리지를 리뷰해 주세요. 코드 변경 사항이 충분히 테스트되었는지 확인하고, 경계 상황을 다루고 있는지 체크해 주세요:\n\n{code_diff}'

        else:
            return f'풀 리퀘스트 제목: "{pr_title}".\n{code_diff}'


# PR에서 변경된 파일 정보 가져오기
def get_changed_files():
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
    GITHUB_PR_NUMBER = os.getenv("PR_NUMBER")
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
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

    if not GITHUB_PR_NUMBER:
        raise ValueError("PR_NUMBER environment variable is missing or None.")
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls/{GITHUB_PR_NUMBER}/commits"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


# Ollama API로 코드 리뷰 요청
def get_ollama_review(code_diff):
    # 환경 변수로부터 입력 받기
    prompt_type = os.getenv("PROMPT_TYPE", PromptType.GENERAL_REVIEW)
    prompt_language = os.getenv("PROMPT_LANGUAGE", "EN")
    pr_title = os.getenv("PR_TITLE")
    pr_body = os.getenv("PR_BODY")
    ollama_model = os.getenv("OLLAMA_MODEL")
    ollama_url = os.getenv("OLLAMA_API_URL")
    headers = {"Content-Type": "application/json"}

    # 프롬프트 생성
    prompt = generate_prompt(prompt_type, pr_title, pr_body, code_diff, prompt_language)

    # 데이터 설정
    data = {
        "model": ollama_model,
        "prompt": prompt,
        "stream": False,
    }

    # Ollama API 호출
    try:
        response = requests.post(
            f"{ollama_url}/api/generate", json=data, headers=headers
        )
        response.raise_for_status()  # 오류 발생 시 예외 처리
        result = response.json()  # JSON 파싱
        print(f"Ollama API response: {result}")
        return result.get("response", "리뷰 결과를 찾을 수 없습니다.")
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}")
        return "Ollama API 호출 실패"


# 코드 리뷰 요청 (GitHub API로 PR에 종합적인 코멘트 추가)
def post_review_comment(commit_id, body):
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
    GITHUB_PR_NUMBER = os.getenv("PR_NUMBER")
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
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
