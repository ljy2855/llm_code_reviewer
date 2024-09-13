# Python 3.12 기반 이미지 사용
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 및 테스트 코드 복사
COPY src/ ./src

# 환경 변수 설정 (필요하다면 추가)
ENV PATH="/usr/local/bin:${PATH}"

# main.py를 실행 가능하도록 설정
RUN chmod +x src/main.py

# 기본 실행 명령
ENTRYPOINT ["python3", "/app/src/main.py"]
