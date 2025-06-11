"""
AI 마케팅 서비스 Flask 애플리케이션
점주를 위한 마케팅 콘텐츠 및 포스터 자동 생성 서비스
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import traceback
from config.config import Config
from services.content_service import ContentService
from services.poster_service import PosterService
from models.request_models import ContentRequest, PosterRequest
def create_app():
    """Flask 애플리케이션 팩토리"""
    app = Flask(__name__)
    app.config.from_object(Config)
    # CORS 설정
    CORS(app)
    # 업로드 폴더 생성
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'temp'), exist_ok=True)
    os.makedirs('templates/poster_templates', exist_ok=True)
    # 서비스 인스턴스 생성
    content_service = ContentService()
    poster_service = PosterService()
    @app.route('/health', methods=['GET'])
    def health_check():
        """헬스 체크 API"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'AI Marketing Service'
        })
    @app.route('/api/content/generate', methods=['POST'])
    def generate_content():
        """
        마케팅 콘텐츠 생성 API
        점주가 입력한 정보를 바탕으로 플랫폼별 맞춤 게시글 생성
        """
        try:
            # 요청 데이터 검증
            if not request.form:
                return jsonify({'error': '요청 데이터가 없습니다.'}), 400
            # 파일 업로드 처리
            uploaded_files = []
            if 'images' in request.files:
                files = request.files.getlist('images')
                for file in files:
                    if file and file.filename:
                        filename = secure_filename(file.filename)
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        unique_filename = f"{timestamp}_{filename}"
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp', unique_filename)
                        file.save(file_path)
                        uploaded_files.append(file_path)
            # 요청 모델 생성
            content_request = ContentRequest(
                category=request.form.get('category', '음식'),
                platform=request.form.get('platform', '인스타그램'),
                image_paths=uploaded_files,
                start_time=request.form.get('start_time'),
                end_time=request.form.get('end_time'),
                store_name=request.form.get('store_name', ''),
                additional_info=request.form.get('additional_info', '')
            )
            # 콘텐츠 생성
            result = content_service.generate_content(content_request)
            # 임시 파일 정리
            for file_path in uploaded_files:
                try:
                    os.remove(file_path)
                except OSError:
                    pass
            return jsonify(result)
        except Exception as e:
            # 에러 발생 시 임시 파일 정리
            for file_path in uploaded_files:
                try:
                    os.remove(file_path)
                except OSError:
                    pass
            app.logger.error(f"콘텐츠 생성 중 오류 발생: {str(e)}")
            app.logger.error(traceback.format_exc())
            return jsonify({'error': f'콘텐츠 생성 중 오류가 발생했습니다: {str(e)}'}), 500
    @app.route('/api/poster/generate', methods=['POST'])
    def generate_poster():
        """
        홍보 포스터 생성 API
        점주가 입력한 정보를 바탕으로 시각적 홍보 포스터 생성
        """
        try:
            # 요청 데이터 검증
            if not request.form:
                return jsonify({'error': '요청 데이터가 없습니다.'}), 400
            # 파일 업로드 처리
            uploaded_files = []
            if 'images' in request.files:
                files = request.files.getlist('images')
                for file in files:
                    if file and file.filename:
                        filename = secure_filename(file.filename)
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        unique_filename = f"{timestamp}_{filename}"
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp', unique_filename)
                        file.save(file_path)
                        uploaded_files.append(file_path)
            # 요청 모델 생성
            poster_request = PosterRequest(
                category=request.form.get('category', '음식'),
                image_paths=uploaded_files,
                start_time=request.form.get('start_time'),
                end_time=request.form.get('end_time'),
                store_name=request.form.get('store_name', ''),
                event_title=request.form.get('event_title', ''),
                discount_info=request.form.get('discount_info', ''),
                additional_info=request.form.get('additional_info', '')
            )
            # 포스터 생성
            result = poster_service.generate_poster(poster_request)
            # 임시 파일 정리
            for file_path in uploaded_files:
                try:
                    os.remove(file_path)
                except OSError:
                    pass
            return jsonify(result)
        except Exception as e:
            # 에러 발생 시 임시 파일 정리
            for file_path in uploaded_files:
                try:
                    os.remove(file_path)
                except OSError:
                    pass
            app.logger.error(f"포스터 생성 중 오류 발생: {str(e)}")
            app.logger.error(traceback.format_exc())
            return jsonify({'error': f'포스터 생성 중 오류가 발생했습니다: {str(e)}'}), 500
    @app.errorhandler(413)
    def too_large(e):
        """파일 크기 초과 에러 처리"""
        return jsonify({'error': '업로드된 파일이 너무 큽니다. (최대 16MB)'}), 413
    @app.errorhandler(500)
    def internal_error(error):
        """내부 서버 에러 처리"""
        return jsonify({'error': '내부 서버 오류가 발생했습니다.'}), 500
    return app
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)