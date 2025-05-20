FROM python:3.10-slim

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치

RUN pip install --no-cache-dir uvicorn fastapi python-dotenv pydantic psycopg2 boto3
RUN pip install pandas numpy google-genai pgvector


# 애플리케이션 코드 복사
COPY . .

# 포트 노출docke
EXPOSE 8000

# 가상 환경 없이 직접 실행
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000" , "--proxy-headers"]