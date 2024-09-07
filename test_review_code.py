import unittest
from unittest.mock import patch, Mock
import os
import requests

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
    def test_get_changed_files(self, mock_post, mock_get):
        # GitHub API에서 변경된 파일 정보를 가져오는 부분을 Mocking
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = [
            {
                "filename": "test_file.py",
                "patch": "diff --git a/test_file.py b/test_file.py",
            }
        ]

        # Ollama API 응답을 Mocking
        mock_post.return_value = Mock(status_code=200)
        mock_post.return_value.json.return_value = {"response": "This is a test review"}

        # 테스트 환경 변수 설정
        set_test_environment()

        # 코드 리뷰 함수 실행
        main()

        # Mock API 호출이 제대로 되었는지 확인
        mock_get.assert_called_with(
            "https://api.github.com/repos/test_owner/test_repo/pulls/1/files",
            headers={
                "Authorization": "Bearer test_token",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )

        mock_post.assert_called_with(
            "https://api.ollama.com/api/generate",
            json={
                "model": "llama3.1:8b",
                "prompt": "Review the following code\ndiff --git a/test_file.py b/test_file.py",
                "stream": False,
            },
            headers={"Content-Type": "application/json"},
        )

        print("Test passed successfully!")


if __name__ == "__main__":
    unittest.main()
