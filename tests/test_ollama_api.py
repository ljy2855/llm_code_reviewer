import unittest
from unittest.mock import patch, Mock
import os
from src.ollama_api import get_ollama_review


class TestOllamaAPI(unittest.TestCase):

    @patch("requests.post")
    def test_get_ollama_review(self, mock_post):
        os.environ["PROMPT_TYPE"] = "GENERAL_REVIEW"
        os.environ["PROMPT_LANGUAGE"] = "EN"
        os.environ["PR_TITLE"] = "Test PR"
        os.environ["PR_BODY"] = "This is a test PR"

        mock_post.return_value = Mock(
            status_code=200,
            json=Mock(return_value={"response": "This is a test review"}),
        )

        code_diff = "diff --git a/test_file.py b/test_file.py"
        review_comment = get_ollama_review(code_diff)

        self.assertEqual(review_comment, "This is a test review")


if __name__ == "__main__":
    unittest.main()
