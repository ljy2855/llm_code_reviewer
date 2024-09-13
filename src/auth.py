import os
import jwt
import time
import requests


# 1. JWT 생성
def generate_jwt():
    # GitHub App 설정
    app_id = os.getenv("APP_ID")
    private_key = os.getenv("APP_PRIVATE_KEY")
    payload = {
        "iat": int(time.time()),  # Issued at time
        "exp": int(time.time()) + (10 * 60),  # JWT 만료 시간 (최대 10분)
        "iss": app_id,  # GitHub App ID
    }

    # RSA SHA256 서명을 사용해 JWT 생성
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token


# 2. App Installation Token 요청
def get_installation_token(jwt_token):
    # 설치 ID 얻기 (여러 개의 설치가 있을 경우 선택 가능)
    installations_url = "https://api.github.com/app/installations"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json",
    }

    response = requests.get(installations_url, headers=headers)
    response.raise_for_status()  # 오류 발생 시 예외 처리
    installations = response.json()

    # 설치된 ID를 얻음 (여기서는 첫 번째 설치를 사용)
    installation_id = installations[0]["id"]

    # Installation Token 요청
    token_url = (
        f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    )
    token_response = requests.post(token_url, headers=headers)
    token_response.raise_for_status()  # 오류 발생 시 예외 처리
    token_data = token_response.json()

    # Access Token 반환
    return token_data["token"]
