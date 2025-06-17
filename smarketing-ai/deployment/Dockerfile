FROM python:3.11-slim

WORKDIR /app

# 경로 수정
COPY smarketing-ai/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY smarketing-ai/ .

# 포트 노출
EXPOSE 5001

# 애플리케이션 실행
CMD ["python", "app.py"]