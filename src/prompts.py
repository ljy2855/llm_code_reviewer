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
