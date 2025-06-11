"""
마케팅 콘텐츠 생성 서비스
AI를 활용하여 플랫폼별 맞춤 게시글 생성
"""
import os
from typing import Dict, Any
from datetime import datetime
from utils.ai_client import AIClient
from utils.image_processor import ImageProcessor
from models.request_models import ContentRequest
class ContentService:
    """마케팅 콘텐츠 생성 서비스 클래스"""
    def __init__(self):
        """서비스 초기화"""
        self.ai_client = AIClient()
        self.image_processor = ImageProcessor()
        # 플랫폼별 콘텐츠 특성 정의
        self.platform_specs = {
            '인스타그램': {
                'max_length': 2200,
                'hashtag_count': 15,
                'style': '감성적이고 시각적',
                'format': '짧은 문장, 해시태그 활용'
            },
            '네이버 블로그': {
                'max_length': 3000,
                'hashtag_count': 10,
                'style': '정보성과 친근함',
                'format': '구조화된 내용, 상세 설명'
            }
        }
        # 카테고리별 키워드 정의
        self.category_keywords = {
            '음식': ['맛집', '신메뉴', '추천', '맛있는', '특별한', '인기'],
            '매장': ['분위기', '인테리어', '편안한', '아늑한', '특별한', '방문'],
            '이벤트': ['할인', '이벤트', '특가', '한정', '기간한정', '혜택']
        }
    def generate_content(self, request: ContentRequest) -> Dict[str, Any]:
        """
        마케팅 콘텐츠 생성
        Args:
            request: 콘텐츠 생성 요청 데이터
        Returns:
            생성된 콘텐츠 정보
        """
        try:
            # 이미지 분석
            image_analysis = self._analyze_images(request.image_paths)
            # AI 프롬프트 생성
            prompt = self._create_content_prompt(request, image_analysis)
            # AI로 콘텐츠 생성
            generated_content = self.ai_client.generate_text(prompt)
            # 해시태그 생성
            hashtags = self._generate_hashtags(request)
            # 최종 콘텐츠 포맷팅
            formatted_content = self._format_content(
                generated_content, 
                hashtags, 
                request.platform
            )
            return {
                'success': True,
                'content': formatted_content,
                'platform': request.platform,
                'category': request.category,
                'generated_at': datetime.now().isoformat(),
                'image_count': len(request.image_paths),
                'image_analysis': image_analysis
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'generated_at': datetime.now().isoformat()
            }
    def _analyze_images(self, image_paths: list) -> Dict[str, Any]:
        """
        업로드된 이미지들 분석
        Args:
            image_paths: 이미지 파일 경로 리스트
        Returns:
            이미지 분석 결과
        """
        analysis_results = []
        for image_path in image_paths:
            try:
                # 이미지 기본 정보 추출
                image_info = self.image_processor.get_image_info(image_path)
                # AI를 통한 이미지 내용 분석
                image_description = self.ai_client.analyze_image(image_path)
                analysis_results.append({
                    'path': image_path,
                    'info': image_info,
                    'description': image_description
                })
            except Exception as e:
                analysis_results.append({
                    'path': image_path,
                    'error': str(e)
                })
        return {
            'total_images': len(image_paths),
            'results': analysis_results
        }
    def _create_content_prompt(self, request: ContentRequest, image_analysis: Dict[str, Any]) -> str:
        """
        AI 콘텐츠 생성을 위한 프롬프트 생성
        Args:
            request: 콘텐츠 생성 요청
            image_analysis: 이미지 분석 결과
        Returns:
            AI 프롬프트 문자열
        """
        platform_spec = self.platform_specs.get(request.platform, self.platform_specs['인스타그램'])
        category_keywords = self.category_keywords.get(request.category, [])
        # 이미지 설명 추출
        image_descriptions = []
        for result in image_analysis.get('results', []):
            if 'description' in result:
                image_descriptions.append(result['description'])
        prompt = f"""
당신은 소상공인을 위한 마케팅 콘텐츠 전문가입니다.
다음 정보를 바탕으로 {request.platform}에 적합한 {request.category} 카테고리의 게시글을 작성해주세요.
**매장 정보:**
- 매장명: {request.store_name or '우리 가게'}
- 카테고리: {request.category}
- 추가 정보: {request.additional_info or '없음'}
**이벤트 정보:**
- 시작 시간: {request.start_time or '상시'}
- 종료 시간: {request.end_time or '상시'}
**이미지 분석 결과:**
{chr(10).join(image_descriptions) if image_descriptions else '이미지 없음'}
**플랫폼 특성:**
- 최대 길이: {platform_spec['max_length']}자
- 스타일: {platform_spec['style']}
- 형식: {platform_spec['format']}
**요구사항:**
1. {request.platform}의 특성에 맞는 톤앤매너 사용
2. {request.category} 카테고리에 적합한 내용 구성
3. 고객의 관심을 끌 수 있는 매력적인 문구 사용
4. 이미지와 연관된 내용으로 작성
5. 자연스럽고 친근한 어조 사용
해시태그는 별도로 생성하므로 본문에는 포함하지 마세요.
"""
        return prompt
    def _generate_hashtags(self, request: ContentRequest) -> list:
        """
        카테고리와 플랫폼에 맞는 해시태그 생성
        Args:
            request: 콘텐츠 생성 요청
        Returns:
            해시태그 리스트
        """
        platform_spec = self.platform_specs.get(request.platform, self.platform_specs['인스타그램'])
        category_keywords = self.category_keywords.get(request.category, [])
        hashtags = []
        # 기본 해시태그
        if request.store_name:
            hashtags.append(f"#{request.store_name.replace(' ', '')}")
        # 카테고리별 해시태그
        hashtags.extend([f"#{keyword}" for keyword in category_keywords[:5]])
        # 공통 해시태그
        common_tags = ['#맛집', '#소상공인', '#로컬맛집', '#일상', '#소통']
        hashtags.extend(common_tags)
        # 플랫폼별 인기 해시태그
        if request.platform == '인스타그램':
            hashtags.extend(['#인스타푸드', '#데일리', '#오늘뭐먹지', '#맛스타그램'])
        elif request.platform == '네이버 블로그':
            hashtags.extend(['#블로그', '#후기', '#추천', '#정보'])
        # 최대 개수 제한
        max_count = platform_spec['hashtag_count']
        return hashtags[:max_count]
    def _format_content(self, content: str, hashtags: list, platform: str) -> str:
        """
        플랫폼에 맞게 콘텐츠 포맷팅
        Args:
            content: 생성된 콘텐츠
            hashtags: 해시태그 리스트
            platform: 플랫폼명
        Returns:
            포맷팅된 최종 콘텐츠
        """
        platform_spec = self.platform_specs.get(platform, self.platform_specs['인스타그램'])
        # 길이 제한 적용
        if len(content) > platform_spec['max_length'] - 100:  # 해시태그 공간 확보
            content = content[:platform_spec['max_length'] - 100] + '...'
        # 플랫폼별 포맷팅
        if platform == '인스타그램':
            # 인스타그램: 본문 + 해시태그
            hashtag_string = ' '.join(hashtags)
            formatted = f"{content}\n\n{hashtag_string}"
        elif platform == '네이버 블로그':
            # 네이버 블로그: 구조화된 형태
            hashtag_string = ' '.join(hashtags)
            formatted = f"{content}\n\n---\n{hashtag_string}"
        else:
            # 기본 형태
            hashtag_string = ' '.join(hashtags)
            formatted = f"{content}\n\n{hashtag_string}"
        return formatted