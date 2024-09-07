import unittest
from unittest.mock import patch, Mock
import os
import requests
import json  # 이 부분을 추가해야 합니다

# 실제 review_code.py의 로직을 가져옵니다
from main import main


# 테스트를 위한 환경변수 설정
def set_test_environment():
    os.environ["GITHUB_TOKEN"] = "test_token"
    os.environ["GITHUB_REPOSITORY"] = "test_owner/test_repo"
    os.environ["GITHUB_PR_NUMBER"] = "1"
    os.environ["GITHUB_OWNER"] = "test_owner"
    os.environ["OLLAMA_MODEL"] = "llama3.1:8b"
    os.environ["PROMT"] = "Review the following code"
    os.environ["OLLAMA_API_URL"] = "https://api.ollama.com"


class TestCodeReview(unittest.TestCase):

    @patch("requests.get")
    @patch("requests.post")
    def test_main_function(self, mock_post, mock_get):
        # Mocking GitHub API에서 변경된 파일 정보를 가져오는 부분
        mock_get.side_effect = [
            Mock(
                status_code=200,
                json=Mock(
                    return_value=[
                        {
                            "filename": "test_file.py",
                            "patch": "diff --git a/test_file.py b/test_file.py",
                        },
                        {
                            "filename": "another_file.py",
                            "patch": "diff --git a/another_file.py b/another_file.py",
                        },
                    ]
                ),
            ),
            Mock(status_code=200, json=Mock(return_value=[{"sha": "commit_sha"}])),
        ]

        # Mock Ollama API 응답
        mock_post.return_value = Mock(
            status_code=200, text=json.dumps({"response": "This is a test review"})
        )

        # 테스트 환경 변수 설정
        set_test_environment()

        # 코드 리뷰 함수 실행
        main()

        # 호출된 인자 검증을 위한 값 가져오기
        get_call_1 = mock_get.call_args_list[0]  # 첫 번째 호출에 대한 인자
        get_call_2 = mock_get.call_args_list[1]  # 두 번째 호출에 대한 인자

        # 첫 번째 호출 검증 (변경된 파일 정보 가져오기)
        self.assertEqual(
            get_call_1[0][0],
            "https://api.github.com/repos/test_owner/test_repo/pulls/1/files",
        )
        self.assertEqual(
            get_call_1[1]["headers"]["Accept"], "application/vnd.github+json"
        )
        self.assertEqual(get_call_1[1]["headers"]["X-GitHub-Api-Version"], "2022-11-28")

        # 두 번째 호출 검증 (PR의 커밋 정보 가져오기)
        self.assertEqual(
            get_call_2[0][0],
            "https://api.github.com/repos/test_owner/test_repo/pulls/1/commits",
        )
        self.assertEqual(
            get_call_2[1]["headers"]["Accept"], "application/vnd.github+json"
        )
        self.assertEqual(get_call_2[1]["headers"]["X-GitHub-Api-Version"], "2022-11-28")

        # Ollama API로 보내진 데이터 검증
        mock_post.assert_called_with(
            "https://api.ollama.com/api/generate",
            json={
                "model": "llama3.1:8b",
                "prompt": "Review the following code\ndiff --git a/test_file.py b/test_file.py\ndiff --git a/another_file.py b/another_file.py",
                "stream": False,
            },
            headers={"Content-Type": "application/json"},
        )

        # PR에 종합적인 리뷰 코멘트를 남기는 부분도 검증
        mock_post.assert_any_call(
            "https://api.github.com/repos/test_owner/test_repo/pulls/1/reviews",
            json={
                "commit_id": "commit_sha",
                "body": "This is a test review",
                "event": "COMMENT",
            },
            headers={
                "Authorization": "Bearer test_token",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )

        print("Test passed successfully!")


if __name__ == "__main__":
    unittest.main()
