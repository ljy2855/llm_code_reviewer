# LLM code reviewer

`GitHub Actions`를 통해 **Pull Request(PR)** 에 대해 자동화된 코드 리뷰를 제공.

## Requriements

- external Ollama server
- Personal Access Token

## How to use

1. Ollama 서버 설정 Ollama 서버는 모델을 통해 코드 변경사항을 통한 리뷰 제공.
   외부 서버를 설정하고 `OLLAMA_API_URL`을 GitHub Secrets에 추가.
   [ollama api docs](https://github.com/ollama/ollama/blob/main/docs/api.md)

2. Personal Access Token 설정 GitHub API을 위해 **Personal Access Token (PAT)**
   을 발급받아, 이를 `MY_PAT` 이름으로 GitHub Secrets에 저장.
   [github api docs](https://docs.github.com/ko/rest/pulls/reviews?apiVersion=2022-11-28#create-a-review-for-a-pull-request)

3. workflow 작성

```yaml
name: 'Use Code Review Action'

on:
  pull_request_target:
    types: [opened] # PR이 열릴 때 트리거

permissions:
  issues: write # GitHub API에서 이슈 및 PR에 코멘트를 달 수 있는 권한 부여

jobs:
  code-review:
    runs-on: ubuntu-latest # 최신 Ubuntu 환경에서 실행

    steps:
      - name: Checkout the code
        uses: actions/checkout@v3 # 코드 체크아웃

      - name: Run external Code Review Action
        uses: ljy2855/llm_code_reviewer@main
        with:
          # fixed fields
          github_owner: ${{ github.repository_owner }} # 레포지토리 소유자
          pr_number: ${{ github.event.pull_request.number }} # PR 번호
          repository: ${{ github.repository }} # 레포지토리 이름

          # you might fill
          github_token: ${{ secrets.MY_PAT }} # GitHub Personal Access Token
          ollama_api_url: ${{ secrets.OLLAMA_API_URL }} # Ollama API URL
          ollama_model: 'llama3.1:8b' # LLM 모델 설정 (예: "llama3.1:8b")
          prompt: 'Review this code :' # 코드 리뷰를 위한 프롬프트 (선택 사항)
```

4. PR open 이후 git actions workflow 작동

![스크린샷 2024-09-08 오전 2 02 52](https://github.com/user-attachments/assets/c991a66a-720d-4d8b-8a11-7cad593f63ad)


github api를 통한 comment 생성
