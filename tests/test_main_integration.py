import unittest
from unittest.mock import patch, Mock
import os
from src.main import main


class TestMainIntegration(unittest.TestCase):

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
            ),  # PR 변경 파일을 확인하는 API 응답
            Mock(
                status_code=200, json=Mock(return_value=[{"sha": "commit_sha"}])
            ),  # PR 커밋 리스트를 가져오는 API 응답
        ]

        mock_post.side_effect = [
            Mock(
                status_code=200,
                json=Mock(return_value={"response": "This is a test review"}),
            ),  # Mock Ollama API 응답
            Mock(
                status_code=200,
                json=Mock(
                    return_value={"response": "Review comment posted successfully"}
                ),
            ),  # Mock GitHub PR comment API 응답
        ]

        # 테스트 환경 변수 설정
        os.environ["GITHUB_TOKEN"] = "test_token"
        os.environ["GITHUB_REPOSITORY"] = "test_owner/test_repo"
        os.environ["PR_NUMBER"] = "1"
        os.environ["GITHUB_OWNER"] = "test_owner"
        os.environ["OLLAMA_MODEL"] = "llama3.1:8b"
        os.environ["OLLAMA_API_URL"] = "https://api.ollama.com"

        # 코드 리뷰 함수 실행
        main()

        # 호출된 인자 검증을 위한 값 가져오기 (첫 번째 Ollama 호출과 두 번째 GitHub 호출)
        post_call_1 = mock_post.call_args_list[0]  # 첫 번째 호출 (Ollama API)
        post_call_2 = mock_post.call_args_list[1]  # 두 번째 호출 (GitHub 리뷰)

        # Ollama API 호출 검증
        self.assertEqual(post_call_1[0][0], "https://api.ollama.com/api/generate")
        self.assertEqual(post_call_1[1]["json"]["model"], "llama3.1:8b")
        self.assertEqual(post_call_1[1]["headers"]["Content-Type"], "application/json")

        # GitHub 리뷰 호출 검증
        self.assertEqual(
            post_call_2[0][0],
            "https://api.github.com/repos/test_owner/test_repo/pulls/1/reviews",
        )
        self.assertEqual(post_call_2[1]["json"]["commit_id"], "commit_sha")
        self.assertEqual(post_call_2[1]["json"]["body"], "This is a test review")
        self.assertEqual(post_call_2[1]["json"]["event"], "COMMENT")

        print("Integration test passed successfully!")


if __name__ == "__main__":
    unittest.main()
