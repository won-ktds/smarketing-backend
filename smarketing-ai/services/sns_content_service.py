"""
SNS 콘텐츠 생성 서비스
"""
import os
from typing import Dict, Any
from datetime import datetime
from utils.ai_client import AIClient
from utils.image_processor import ImageProcessor
from models.request_models import SnsContentGetRequest


class SnsContentService:

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

        # 톤앤매너별 스타일
        self.tone_styles = {
            '친근한': '반말, 이모티콘 활용, 편안한 어조',
            '정중한': '존댓말, 격식 있는 표현, 신뢰감 있는 어조',
            '재미있는': '유머 섞인 표현, 트렌디한 말투, 참신한 비유',
            '전문적인': '전문 용어 활용, 체계적 설명, 신뢰성 강조'
        }

        # 감정 강도별 표현
        self.emotion_levels = {
            '약함': '은은하고 차분한 표현',
            '보통': '적당히 활기찬 표현',
            '강함': '매우 열정적이고 강렬한 표현'
        }

    def generate_sns_content(self, request: SnsContentGetRequest) -> Dict[str, Any]:
        """
        SNS 콘텐츠 생성 (HTML 형식 반환)
        """
        try:
            # 이미지 다운로드 및 분석
            image_analysis = self._analyze_images_from_urls(request.images)

            # AI 프롬프트 생성
            prompt = self._create_sns_prompt(request, image_analysis)

            # AI로 콘텐츠 생성
            generated_content = self.ai_client.generate_text(prompt)

            # HTML 형식으로 포맷팅
            html_content = self._format_to_html(generated_content, request)

            return {
                'success': True,
                'content': html_content
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _analyze_images_from_urls(self, image_urls: list) -> Dict[str, Any]:
        """
        URL에서 이미지를 다운로드하고 분석
        """
        analysis_results = []
        temp_files = []

        try:
            for image_url in image_urls:
                # 이미지 다운로드
                temp_path = self.ai_client.download_image_from_url(image_url)
                if temp_path:
                    temp_files.append(temp_path)

                    # 이미지 분석
                    try:
                        image_info = self.image_processor.get_image_info(temp_path)
                        image_description = self.ai_client.analyze_image(temp_path)

                        analysis_results.append({
                            'url': image_url,
                            'info': image_info,
                            'description': image_description
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

    def _create_sns_prompt(self, request: SnsContentGetRequest, image_analysis: Dict[str, Any]) -> str:
        """
        SNS 콘텐츠 생성을 위한 AI 프롬프트 생성
        """
        platform_spec = self.platform_specs.get(request.platform, self.platform_specs['인스타그램'])
        tone_style = self.tone_styles.get(request.toneAndManner, '정중하고 재밌는 어조')
        emotion_level = self.emotion_levels.get(request.emotionIntensity, '적당한 강도')

        # 이미지 설명 추출
        image_descriptions = []
        for result in image_analysis.get('results', []):
            if 'description' in result:
                image_descriptions.append(result['description'])

        prompt = f"""
당신은 소상공인을 위한 SNS 마케팅 콘텐츠 전문가입니다.
다음 정보를 바탕으로 {request.platform}에 적합한 게시글을 작성해주세요.

**게시물 정보:**
- 제목: {request.title}
- 카테고리: {request.category}
- 콘텐츠 타입: {request.contentType}

**스타일 요구사항:**
- 톤앤매너: {request.toneAndManner} ({tone_style})
- 감정 강도: {request.emotionIntensity} ({emotion_level})
- 특별 요구사항: {request.requirement or '없음'}

**메뉴 정보:**
- 메뉴명: {request.menuName or '없음'}

**이벤트 정보:**
- 이벤트명: {request.eventName or '없음'}
- 시작일: {request.startDate or '없음'}
- 종료일: {request.endDate or '없음'}

**이미지 분석 결과:**
{chr(10).join(image_descriptions) if image_descriptions else '이미지 없음'}

**플랫폼 특성:**
- 최대 길이: {platform_spec['max_length']}자
- 스타일: {platform_spec['style']}
- 형식: {platform_spec['format']}

**요구사항:**
1. 중요 => {request.platform}의 특성에 맞는 내용 구성
2. {request.category} 카테고리에 적합한 내용 구성
3. 고객의 관심을 끌 수 있는 매력적인 문구 사용
4. 이미지와 연관된 내용으로 작성
5. 지정된 톤앤매너와 감정 강도에 맞게 작성

본문과 해시태그를 모두 포함하여 완성된 게시글을 작성해주세요.
"""
        return prompt

    def _format_to_html(self, content: str, request: SnsContentGetRequest) -> str:
        """
        생성된 콘텐츠를 HTML 형식으로 포맷팅
        """
        # 1. literal \n 문자열을 실제 줄바꿈으로 변환
        content = content.replace('\\n', '\n')

        # 2. 실제 줄바꿈을 <br> 태그로 변환
        content = content.replace('\n', '<br>')

        # 3. 추가 정리: \r, 여러 공백 정리
        content = content.replace('\\r', '').replace('\r', '')

        # 4. 여러 개의 <br> 태그를 하나로 정리
        import re
        content = re.sub(r'(<br>\s*){3,}', '<br><br>', content)

        # 5. 해시태그를 파란색으로 스타일링
        content = re.sub(r'(#[\w가-힣]+)', r'<span style="color: #1DA1F2; font-weight: bold;">\1</span>', content)

        # 전체 HTML 구조
        html_content = f"""
    <div style="font-family: 'Noto Sans KR', Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 600px;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 10px 10px 0 0; text-align: center;">
            <h3 style="margin: 0; font-size: 18px;">{request.platform} 게시물</h3>
        </div>
        <div style="background: white; padding: 20px; border-radius: 0 0 10px 10px; border: 1px solid #e1e8ed;">
            <div style="font-size: 16px; color: #333; line-height: 1.8;">
                {content}
            </div>
            {self._add_metadata_html(request)}
        </div>
    </div>
    """
        return html_content

    def _add_metadata_html(self, request: SnsContentGetRequest) -> str:
        """
        메타데이터를 HTML에 추가
        """
        metadata_html = '<div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #e1e8ed; font-size: 12px; color: #666;">'

        if request.menuName:
            metadata_html += f'<div><strong>메뉴:</strong> {request.menuName}</div>'

        if request.eventName:
            metadata_html += f'<div><strong>이벤트:</strong> {request.eventName}</div>'

        if request.startDate and request.endDate:
            metadata_html += f'<div><strong>기간:</strong> {request.startDate} ~ {request.endDate}</div>'

        metadata_html += f'<div><strong>카테고리:</strong> {request.category}</div>'
        metadata_html += f'<div><strong>생성일:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>'
        metadata_html += '</div>'

        return metadata_html
