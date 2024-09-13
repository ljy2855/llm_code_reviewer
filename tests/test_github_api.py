import unittest
from unittest.mock import patch, Mock
import os
from src.github_api import get_changed_files, get_pr_commits


class TestGitHubAPI(unittest.TestCase):

    @patch("requests.get")
    def test_get_changed_files(self, mock_get):
        mock_get.return_value = Mock(
            status_code=200,
            json=Mock(
                return_value=[
                    {
                        "filename": "test_file.py",
                        "patch": "diff --git a/test_file.py b/test_file.py",
                    }
                ]
            ),
        )

        files = get_changed_files()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0]["filename"], "test_file.py")

    @patch("requests.get")
    def test_get_pr_commits(self, mock_get):
        mock_get.return_value = Mock(
            status_code=200,
            json=Mock(return_value=[{"sha": "commit_sha"}]),
        )

        commits = get_pr_commits()
        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0]["sha"], "commit_sha")


if __name__ == "__main__":
    unittest.main()
