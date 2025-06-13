"""
Flask 애플리케이션 설정
환경변수를 통한 설정 관리
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """애플리케이션 설정 클래스"""
    # Flask 기본 설정
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    # 파일 업로드 설정
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH') or 16 * 1024 * 1024)  # 16MB
    # AI API 설정
    CLAUDE_API_KEY = os.environ.get('CLAUDE_API_KEY')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    # 지원되는 파일 확장자
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    # 템플릿 설정
    POSTER_TEMPLATE_PATH = 'templates/poster_templates'

    @staticmethod
    def allowed_file(filename):
        """업로드 파일 확장자 검증"""
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
