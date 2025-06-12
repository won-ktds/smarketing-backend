"""
포스터 생성 서비스
OpenAI를 사용한 이미지 생성 (한글 프롬프트)
"""
import os
from typing import Dict, Any
from datetime import datetime
from utils.ai_client import AIClient
from utils.image_processor import ImageProcessor
from models.request_models import PosterContentGetRequest


class PosterService:
    """포스터 생성 서비스 클래스"""

    def __init__(self):
        """서비스 초기화"""
        self.ai_client = AIClient()
        self.image_processor = ImageProcessor()

        # 포토 스타일별 프롬프트
        self.photo_styles = {
            '미니멀': '미니멀하고 깔끔한 디자인, 단순함, 여백 활용',
            '모던': '현대적이고 세련된 디자인, 깔끔한 레이아웃',
            '빈티지': '빈티지 느낌, 레트로 스타일, 클래식한 색감',
            '컬러풀': '다채로운 색상, 밝고 생동감 있는 컬러',
            '우아한': '우아하고 고급스러운 느낌, 세련된 분위기',
            '캐주얼': '친근하고 편안한 느낌, 접근하기 쉬운 디자인'
        }

        # 카테고리별 이미지 스타일
        self.category_styles = {
            '음식': '음식 사진, 먹음직스러운, 맛있어 보이는',
            '매장': '레스토랑 인테리어, 아늑한 분위기',
            '이벤트': '홍보용 디자인, 눈길을 끄는',
            '메뉴': '메뉴 디자인, 정리된 레이아웃',
            '할인': '세일 포스터, 할인 디자인'
        }

        # 톤앤매너별 디자인 스타일
        self.tone_styles = {
            '친근한': '따뜻하고 친근한 색감, 부드러운 느낌',
            '정중한': '격식 있고 신뢰감 있는 디자인',
            '재미있는': '밝고 유쾌한 분위기, 활기찬 색상',
            '전문적인': '전문적이고 신뢰할 수 있는 디자인'
        }

        # 감정 강도별 디자인
        self.emotion_designs = {
            '약함': '은은하고 차분한 색감, 절제된 표현',
            '보통': '적당히 활기찬 색상, 균형잡힌 디자인',
            '강함': '강렬하고 임팩트 있는 색상, 역동적인 디자인'
        }

    def generate_poster(self, request: PosterContentGetRequest) -> Dict[str, Any]:
        """
        포스터 생성 (OpenAI 이미지 URL 반환)
        """
        try:
            # 참조 이미지 분석 (있는 경우)
            image_analysis = self._analyze_reference_images(request.images)

            # 포스터 생성 프롬프트 생성
            prompt = self._create_poster_prompt(request, image_analysis)

            # OpenAI로 이미지 생성
            image_url = self.ai_client.generate_image_with_openai(prompt, "1024x1024")

            return {
                'success': True,
                'content': image_url
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _analyze_reference_images(self, image_urls: list) -> Dict[str, Any]:
        """
        참조 이미지들 분석
        """
        if not image_urls:
            return {'total_images': 0, 'results': []}

        analysis_results = []
        temp_files = []

        try:
            for image_url in image_urls:
                # 이미지 다운로드
                temp_path = self.ai_client.download_image_from_url(image_url)
                if temp_path:
                    temp_files.append(temp_path)

                    try:
                        # 이미지 분석
                        image_description = self.ai_client.analyze_image(temp_path)
                        # 색상 분석
                        colors = self.image_processor.analyze_colors(temp_path, 3)

                        analysis_results.append({
                            'url': image_url,
                            'description': image_description,
                            'dominant_colors': colors
                        })
                    except Exception as e:
                        analysis_results.append({
                            'url': image_url,
                            'error': str(e)
                        })

            return {
                'total_images': len(image_urls),
                'results': analysis_results
            }

        finally:
            # 임시 파일 정리
            for temp_file in temp_files:
                try:
                    os.remove(temp_file)
                except:
                    pass

    def _create_poster_prompt(self, request: PosterContentGetRequest, image_analysis: Dict[str, Any]) -> str:
        """
        포스터 생성을 위한 AI 프롬프트 생성 (한글)
        """
        # 기본 스타일 설정
        photo_style = self.photo_styles.get(request.photoStyle, '현대적이고 깔끔한 디자인')
        category_style = self.category_styles.get(request.category, '홍보용 디자인')
        tone_style = self.tone_styles.get(request.toneAndManner, '친근하고 따뜻한 느낌')
        emotion_design = self.emotion_designs.get(request.emotionIntensity, '적당히 활기찬 디자인')

        # 참조 이미지 설명
        reference_descriptions = []
        for result in image_analysis.get('results', []):
            if 'description' in result:
                reference_descriptions.append(result['description'])

        # 색상 정보
        color_info = ""
        if image_analysis.get('results'):
            colors = image_analysis['results'][0].get('dominant_colors', [])
            if colors:
                color_info = f"참조 색상 팔레트: {colors[:3]}을 활용한 조화로운 색감"

        prompt = f"""
한국의 음식점/카페를 위한 전문적인 홍보 포스터를 디자인해주세요.

**메인 콘텐츠:**
- 제목: "{request.title}"
- 카테고리: {request.category}
- 콘텐츠 타입: {request.contentType}

**디자인 스타일 요구사항:**
- 포토 스타일: {photo_style}
- 카테고리 스타일: {category_style}
- 톤앤매너: {tone_style}
- 감정 강도: {emotion_design}

**메뉴 정보:**
- 메뉴명: {request.menuName or '없음'}

**이벤트 정보:**
- 이벤트명: {request.eventName or '특별 프로모션'}
- 시작일: {request.startDate or '지금'}
- 종료일: {request.endDate or '한정 기간'}

**특별 요구사항:**
{request.requirement or '눈길을 끄는 전문적인 디자인'}

**참조 이미지 설명:**
{chr(10).join(reference_descriptions) if reference_descriptions else '참조 이미지 없음'}

{color_info}

**디자인 가이드라인:**
- 한국 음식점/카페에 적합한 깔끔하고 현대적인 레이아웃
- 한글 텍스트 요소를 자연스럽게 포함
- 가독성이 좋은 전문적인 타이포그래피
- 명확한 대비로 읽기 쉽게 구성
- 소셜미디어 공유에 적합한 크기
- 저작권이 없는 오리지널 디자인
- 음식점에 어울리는 맛있어 보이는 색상 조합
- 고객의 시선을 끄는 매력적인 비주얼

고객들이 음식점을 방문하고 싶게 만드는 시각적으로 매력적인 포스터를 만들어주세요.
텍스트는 한글로, 전체적인 분위기는 한국적 감성에 맞게 디자인해주세요.
"""
        return prompt
