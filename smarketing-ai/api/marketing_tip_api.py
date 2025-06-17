"""
마케팅 팁 생성 API 엔드포인트
Java 서비스와 연동되는 API
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
import logging

from services.marketing_tip_service import MarketingTipService
from models.marketing_tip_models import MarketingTipGenerateRequest, MarketingTipResponse

logger = logging.getLogger(__name__)

# Blueprint 생성
marketing_tip_bp = Blueprint('marketing_tip', __name__)

# 서비스 인스턴스
marketing_tip_service = MarketingTipService()


@marketing_tip_bp.route('/api/v1/generate-marketing-tip', methods=['POST'])
def generate_marketing_tip():
    """
    AI 마케팅 팁 생성 API
    Java 서비스에서 호출하는 엔드포인트
    """
    try:
        # 요청 데이터 검증
        if not request.is_json:
            return jsonify({
                'tip': '',
                'status': 'error',
                'message': 'Content-Type이 application/json이어야 합니다.',
                'generated_at': '',
                'store_name': '',
                'business_type': '',
                'ai_model': ''
            }), 400
        
        data = request.get_json()
        if not data:
            return jsonify({
                'tip': '',
                'status': 'error', 
                'message': '요청 데이터가 없습니다.',
                'generated_at': '',
                'store_name': '',
                'business_type': '',
                'ai_model': ''
            }), 400
        
        # 필수 필드 검증
        if 'store_name' not in data or not data['store_name']:
            return jsonify({
                'tip': '',
                'status': 'error',
                'message': '매장명(store_name)은 필수입니다.',
                'generated_at': '',
                'store_name': '',
                'business_type': '',
                'ai_model': ''
            }), 400
        
        if 'business_type' not in data or not data['business_type']:
            return jsonify({
                'tip': '',
                'status': 'error',
                'message': '업종(business_type)은 필수입니다.',
                'generated_at': '',
                'store_name': '',
                'business_type': '',
                'ai_model': ''
            }), 400
        
        logger.info(f"마케팅 팁 생성 요청: {data.get('store_name', 'Unknown')}")
        
        # 요청 모델 생성
        try:
            request_model = MarketingTipGenerateRequest(**data)
        except ValueError as e:
            return jsonify({
                'tip': '',
                'status': 'error',
                'message': f'요청 데이터 형식이 올바르지 않습니다: {str(e)}',
                'generated_at': '',
                'store_name': data.get('store_name', ''),
                'business_type': data.get('business_type', ''),
                'ai_model': ''
            }), 400
        
        # 매장 정보 구성
        store_data = {
            'store_name': request_model.store_name,
            'business_type': request_model.business_type,
            'location': request_model.location or '',
            'seat_count': request_model.seat_count or 0
        }
        
        # 마케팅 팁 생성
        result = marketing_tip_service.generate_marketing_tip(
            store_data=store_data,
        )
        
        logger.info(f"마케팅 팁 생성 완료: {result.get('store_name', 'Unknown')}")
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"마케팅 팁 생성 API 오류: {str(e)}")
        
        return jsonify({
            'tip': '죄송합니다. 일시적인 오류로 마케팅 팁을 생성할 수 없습니다. 잠시 후 다시 시도해주세요.',
            'status': 'error',
            'message': f'서버 오류가 발생했습니다: {str(e)}',
            'generated_at': '',
            'store_name': data.get('store_name', '') if 'data' in locals() else '',
            'business_type': data.get('business_type', '') if 'data' in locals() else '',
            'ai_model': 'error'
        }), 500


@marketing_tip_bp.route('/api/v1/health', methods=['GET'])
def health_check():
    """
    헬스체크 API
    """
    return jsonify({
        'status': 'healthy',
        'service': 'marketing-tip-api',
        'timestamp': datetime.now().isoformat()
    }), 200