from github_api import get_changed_files, get_pr_commits, post_review_comment
from ollama_api import get_ollama_review
from auth import get_access_token


def main():

    access_token = get_access_token()
    # PR에서 변경된 파일 정보 가져오기
    changed_files = get_changed_files(access_token)

    # PR에서 커밋 리스트 가져오기
    commits = get_pr_commits(access_token)

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
        post_review_comment(commit_id, review_comment, access_token)
    else:
        print("코드 변경 사항이 없습니다.")


if __name__ == "__main__":
    main()
