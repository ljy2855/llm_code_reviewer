# LLM code reviewer

Provides **automated code reviews** for Pull Requests (PR) using `GitHub Actions`

## Requriements

- External Ollama server

## How to use

1. Setup Ollama Server (api server)

    The Ollama server provides reviews using LLM model. Set up the external Ollama server and add the `OLLAMA_API_URL` to your GitHub Secrets.

   [Ollama API Docs](https://github.com/ollama/ollama/blob/main/docs/api.md)

    **Example:** `https://ollama-server-url/api`
2. Write workflow script

```yaml
name: 'Test Container Action'

on:
  pull_request:
    types: [opened] # PR open시 자동 코드 리뷰 요청

permissions:
  contents: read   # 콘텐츠 접근 권한 (PR 변경 사항 읽기)
  pull-requests: write # PR comment 작성 권한

jobs:
  test-action:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:

      - name: Run Container Action
        uses: ljy2855/llm_code_reviewer@v1
        with:
          # fixed field
          github_token: ${{ secrets.GITHUB_TOKEN }}
          github_owner: ${{ github.repository_owner }}
          github_repository: ${{ github.repository }}
          pr_number: ${{ github.event.pull_request.number }}
          pr_title: ${{ github.event.pull_request.title }}
          pr_body: ${{ github.event.pull_request.body }}

          # you might fill
          ollama_api_url: ${{ secrets.OLLAMA_API_URL }}
          ollama_model: 'llama3.1:8b'

          # optional field
          prompt_type: 'GENERAL_REVIEW'
          prompt_language: 'EN' 

```


**Field Description**
| Field             | Default Value     | Description                                                                                                      | Required |
|-------------------|-------------------|------------------------------------------------------------------------------------------------------------------|----------|
| `github_token`     | N/A               | The GitHub token for authentication, typically set as `${{ secrets.GITHUB_TOKEN }}`.                              | Yes      |
| `github_owner`     | N/A               | The owner of the repository.                                                                                     | Yes      |
| `github_repository`| N/A               | The name of the repository.                                                                                      | Yes      |
| `pr_number`        | N/A               | The number of the pull request.                                                                                  | Yes      |
| `pr_title`         | N/A               | The title of the pull request.                                                                                   | Yes      |
| `pr_body`          | N/A               | The body/description of the pull request.                                                                        | Yes      |
| `ollama_api_url`   | N/A               | The base URL of the Ollama API for generating the review.                                                        | Yes      |
| `ollama_model`     | `llama3.1:8b`     | The LLM model used for generating the review comment.                                                            | Yes      |
| `prompt_type`      | `GENERAL_REVIEW`  | Defines the type of review: `GENERAL_REVIEW`, `SECURITY_REVIEW`, `FUNCTIONALITY_REVIEW`, `CODE_STYLE_REVIEW`, `TEST_COVERAGE_REVIEW` | No       |
| `prompt_language`  | `EN`              | Specifies the language for the review comment (e.g., `EN`, `KR`).                                                | No       |


3. Workflow Run

![스크린샷 2024-09-08 오전 2 02 52](https://github.com/user-attachments/assets/c991a66a-720d-4d8b-8a11-7cad593f63ad)


