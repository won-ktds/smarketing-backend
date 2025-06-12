# 1. Dockerfile에 한글 폰트 추가
FROM python:3.11-slim

WORKDIR /app

# 시스템 패키지 및 한글 폰트 설치
RUN apt-get update && apt-get install -y \
    fonts-dejavu-core \
    fonts-noto-cjk \
    fonts-nanum \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 추가 한글 폰트 다운로드 (선택사항)
RUN mkdir -p /app/fonts && \
    wget -O /app/fonts/NotoSansKR-Bold.ttf \
    "https://fonts.gstatic.com/s/notosanskr/v13/PbykFmXiEBPT4ITbgNA5Cgm20xz64px_1hVWr0wuPNGmlQNMEfD4.ttf"

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 업로드 및 포스터 디렉토리 생성
RUN mkdir -p uploads/temp uploads/posters templates/poster_templates

# 포트 노출
EXPOSE 5000

# 애플리케이션 실행
CMD ["python", "app.py"]