# Docker 이미지 기반 (예: Python 3.9)
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지를 설치
COPY requirements.txt .
RUN pip install -r requirements.txt

# 필요한 스크립트와 파일을 복사
COPY main.py .

# 환경 변수 설정 (필요하다면 추가)
ENV PATH="/usr/local/bin:${PATH}"

# GitHub Action의 엔트리포인트 설정
CMD ["python3", "/app/main.py"]
