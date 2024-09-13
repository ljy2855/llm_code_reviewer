import os
import requests
from prompts import generate_prompt, PromptType


# Ollama API로 코드 리뷰 요청
def get_ollama_review(code_diff):
    prompt_type = os.getenv("PROMPT_TYPE", PromptType.GENERAL_REVIEW)
    prompt_language = os.getenv("PROMPT_LANGUAGE", "EN")
    pr_title = os.getenv("PR_TITLE")
    pr_body = os.getenv("PR_BODY")
    ollama_model = os.getenv("OLLAMA_MODEL")
    ollama_url = os.getenv("OLLAMA_API_URL")
    headers = {"Content-Type": "application/json"}

    # 프롬프트 생성
    prompt = generate_prompt(prompt_type, pr_title, pr_body, code_diff, prompt_language)

    # Ollama API 호출
    data = {
        "model": ollama_model,
        "prompt": prompt,
        "stream": False,
    }

    response = requests.post(f"{ollama_url}/api/generate", json=data, headers=headers)
    response.raise_for_status()
    result = response.json()
    print(f"Ollama API response: {result}")
    return result.get("response", "리뷰 결과를 찾을 수 없습니다.")
