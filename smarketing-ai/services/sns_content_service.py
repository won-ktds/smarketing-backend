"""
SNS 콘텐츠 생성 서비스 (플랫폼 특화 개선)
"""
import os
from typing import Dict, Any, List, Tuple
from datetime import datetime
from utils.ai_client import AIClient
from utils.image_processor import ImageProcessor
from models.request_models import SnsContentGetRequest


class SnsContentService:

    def __init__(self):
        """서비스 초기화"""
        self.ai_client = AIClient()
        self.image_processor = ImageProcessor()

        # 플랫폼별 콘텐츠 특성 정의 (대폭 개선)
        self.platform_specs = {
            '인스타그램': {
                'max_length': 2200,
                'hashtag_count': 15,
                'style': '감성적이고 시각적',
                'format': '짧은 문장, 해시태그 활용',
                'content_structure': '후킹 문장 → 스토리텔링 → 행동 유도 → 해시태그',
                'writing_tips': [
                    '첫 문장으로 관심 끌기',
                    '이모티콘을 적절히 활용',
                    '줄바꿈으로 가독성 높이기',
                    '개성 있는 말투 사용',
                    '팔로워와의 소통 유도'
                ],
                'hashtag_strategy': [
                    '브랜딩 해시태그 포함',
                    '지역 기반 해시태그',
                    '트렌딩 해시태그 활용',
                    '음식 관련 인기 해시태그',
                    '감정 표현 해시태그'
                ],
                'call_to_action': ['팔로우', '댓글', '저장', '공유', '방문']
            },
            '네이버 블로그': {
                'max_length': 3000,
                'hashtag_count': 10,
                'style': '정보성과 친근함',
                'format': '구조화된 내용, 상세 설명',
                'content_structure': '제목 → 인트로 → 본문(구조화) → 마무리',
                'writing_tips': [
                    '검색 키워드 자연스럽게 포함',
                    '단락별로 소제목 활용',
                    '구체적인 정보 제공',
                    '후기/리뷰 형식 활용',
                    '지역 정보 상세히 기술'
                ],
                'seo_keywords': [
                    '맛집', '리뷰', '추천', '후기',
                    '메뉴', '가격', '위치', '분위기',
                    '데이트', '모임', '가족', '혼밥'
                ],
                'call_to_action': ['방문', '예약', '문의', '공감', '이웃추가'],
                'image_placement_strategy': [
                    '매장 외관 → 인테리어 → 메뉴판 → 음식 → 분위기',
                    '텍스트 2-3문장마다 이미지 배치',
                    '이미지 설명은 간결하고 매력적으로',
                    '마지막에 대표 이미지로 마무리'
                ]
            }
        }

        # 톤앤매너별 스타일 (플랫폼별 세분화)
        self.tone_styles = {
            '친근한': {
                '인스타그램': '반말, 친구같은 느낌, 이모티콘 많이 사용',
                '네이버 블로그': '존댓말이지만 따뜻하고 친근한 어조'
            },
            '정중한': {
                '인스타그램': '정중하지만 접근하기 쉬운 어조',
                '네이버 블로그': '격식 있고 신뢰감 있는 리뷰 스타일'
            },
            '재미있는': {
                '인스타그램': '유머러스하고 트렌디한 표현',
                '네이버 블로그': '재미있는 에피소드가 포함된 후기'
            },
            '전문적인': {
                '인스타그램': '전문성을 어필하되 딱딱하지 않게',
                '네이버 블로그': '전문가 관점의 상세한 분석과 평가'
            }
        }

        # 카테고리별 플랫폼 특화 키워드
        self.category_keywords = {
            '음식': {
                '인스타그램': ['#맛스타그램', '#음식스타그램', '#먹스타그램', '#맛집', '#foodstagram'],
                '네이버 블로그': ['맛집 리뷰', '음식 후기', '메뉴 추천', '맛집 탐방', '식당 정보']
            },
            '매장': {
                '인스타그램': ['#카페스타그램', '#인테리어', '#분위기맛집', '#데이트장소'],
                '네이버 블로그': ['카페 추천', '분위기 좋은 곳', '인테리어 구경', '모임장소']
            },
            '이벤트': {
                '인스타그램': ['#이벤트', '#프로모션', '#할인', '#특가'],
                '네이버 블로그': ['이벤트 소식', '할인 정보', '프로모션 안내', '특별 혜택']
            }
        }

        # 감정 강도별 표현
        self.emotion_levels = {
            '약함': '은은하고 차분한 표현',
            '보통': '적당히 활기찬 표현',
            '강함': '매우 열정적이고 강렬한 표현'
        }

        # 이미지 타입 분류를 위한 키워드
        self.image_type_keywords = {
            '매장외관': ['외관', '건물', '간판', '입구', '외부'],
            '인테리어': ['내부', '인테리어', '좌석', '테이블', '분위기', '장식'],
            '메뉴판': ['메뉴', '가격', '메뉴판', '메뉴보드', 'menu'],
            '음식': ['음식', '요리', '메뉴', '디저트', '음료', '플레이팅'],
            '사람': ['사람', '고객', '직원', '사장', '요리사'],
            '기타': ['기타', '일반', '전체']
        }

    def generate_sns_content(self, request: SnsContentGetRequest) -> Dict[str, Any]:
        """
        SNS 콘텐츠 생성 (플랫폼별 특화)
        """
        try:
            # 이미지 다운로드 및 분석
            image_analysis = self._analyze_images_from_urls(request.images)

            # 네이버 블로그인 경우 이미지 배치 계획 생성
            image_placement_plan = None
            if request.platform == '네이버 블로그':
                image_placement_plan = self._create_image_placement_plan(image_analysis, request)

            # 플랫폼별 특화 프롬프트 생성
            prompt = self._create_platform_specific_prompt(request, image_analysis, image_placement_plan)

            # AI로 콘텐츠 생성
            generated_content = self.ai_client.generate_text(prompt, max_tokens=1500)

            # 플랫폼별 후처리
            processed_content = self._post_process_content(generated_content, request)

            # HTML 형식으로 포맷팅
            html_content = self._format_to_html(processed_content, request, image_placement_plan)

            result = {
                'success': True,
                'content': html_content
            }

            # 네이버 블로그인 경우 이미지 배치 가이드라인 추가
            if request.platform == '네이버 블로그' and image_placement_plan:
                result['image_placement_guide'] = image_placement_plan

            return result

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _analyze_images_from_urls(self, image_urls: list) -> Dict[str, Any]:
        """
        URL에서 이미지를 다운로드하고 분석 (이미지 타입 분류 추가)
        """
        analysis_results = []
        temp_files = []

        try:
            for i, image_url in enumerate(image_urls):
                # 이미지 다운로드
                temp_path = self.ai_client.download_image_from_url(image_url)
                if temp_path:
                    temp_files.append(temp_path)

                    # 이미지 분석
                    try:
                        image_info = self.image_processor.get_image_info(temp_path)
                        image_description = self.ai_client.analyze_image(temp_path)

                        # 이미지 타입 분류
                        image_type = self._classify_image_type(image_description)

                        analysis_results.append({
                            'index': i,
                            'url': image_url,
                            'info': image_info,
                            'description': image_description,
                            'type': image_type
                        })
                    except Exception as e:
                        analysis_results.append({
                            'index': i,
                            'url': image_url,
                            'error': str(e),
                            'type': '기타'
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

    def _classify_image_type(self, description: str) -> str:
        """
        이미지 설명을 바탕으로 이미지 타입 분류
        """
        description_lower = description.lower()

        for image_type, keywords in self.image_type_keywords.items():
            for keyword in keywords:
                if keyword in description_lower:
                    return image_type

        return '기타'

    def _create_image_placement_plan(self, image_analysis: Dict[str, Any], request: SnsContentGetRequest) -> Dict[
        str, Any]:
        """
        네이버 블로그용 이미지 배치 계획 생성
        """
        images = image_analysis.get('results', [])
        if not images:
            return None

        # 이미지 타입별 분류
        categorized_images = {
            '매장외관': [],
            '인테리어': [],
            '메뉴판': [],
            '음식': [],
            '사람': [],
            '기타': []
        }

        for img in images:
            img_type = img.get('type', '기타')
            categorized_images[img_type].append(img)

        # 블로그 구조에 따른 이미지 배치 계획
        placement_plan = {
            'structure': [
                {
                    'section': '인트로',
                    'description': '첫인상과 방문 동기',
                    'recommended_images': [],
                    'placement_guide': '매장 외관이나 대표적인 음식 사진으로 시작'
                },
                {
                    'section': '매장 정보',
                    'description': '위치, 분위기, 인테리어 소개',
                    'recommended_images': [],
                    'placement_guide': '매장 외관 → 내부 인테리어 순서로 배치'
                },
                {
                    'section': '메뉴 소개',
                    'description': '주문한 메뉴와 상세 후기',
                    'recommended_images': [],
                    'placement_guide': '메뉴판 → 실제 음식 사진 순서로 배치'
                },
                {
                    'section': '총평',
                    'description': '재방문 의향과 추천 이유',
                    'recommended_images': [],
                    'placement_guide': '가장 매력적인 음식 사진이나 전체 분위기 사진'
                }
            ],
            'image_sequence': [],
            'usage_guide': []
        }

        # 각 섹션에 적절한 이미지 배정
        # 인트로: 매장외관 또는 대표 음식
        if categorized_images['매장외관']:
            placement_plan['structure'][0]['recommended_images'].extend(categorized_images['매장외관'][:1])
        elif categorized_images['음식']:
            placement_plan['structure'][0]['recommended_images'].extend(categorized_images['음식'][:1])

        # 매장 정보: 외관 + 인테리어
        placement_plan['structure'][1]['recommended_images'].extend(categorized_images['매장외관'])
        placement_plan['structure'][1]['recommended_images'].extend(categorized_images['인테리어'])

        # 메뉴 소개: 메뉴판 + 음식
        placement_plan['structure'][2]['recommended_images'].extend(categorized_images['메뉴판'])
        placement_plan['structure'][2]['recommended_images'].extend(categorized_images['음식'])

        # 총평: 남은 음식 사진 또는 기타
        remaining_food = [img for img in categorized_images['음식']
                          if img not in placement_plan['structure'][2]['recommended_images']]
        placement_plan['structure'][3]['recommended_images'].extend(remaining_food[:1])
        placement_plan['structure'][3]['recommended_images'].extend(categorized_images['기타'][:1])

        # 전체 이미지 순서 생성
        for section in placement_plan['structure']:
            for img in section['recommended_images']:
                if img not in placement_plan['image_sequence']:
                    placement_plan['image_sequence'].append(img)

        # 사용 가이드 생성
        placement_plan['usage_guide'] = [
            "📸 이미지 배치 가이드라인:",
            "1. 각 섹션마다 2-3문장의 설명 후 이미지 삽입",
            "2. 이미지마다 간단한 설명 텍스트 추가",
            "3. 음식 사진은 가장 맛있어 보이는 각도로 배치",
            "4. 마지막에 전체적인 분위기를 보여주는 사진으로 마무리"
        ]

        return placement_plan

    def _create_platform_specific_prompt(self, request: SnsContentGetRequest, image_analysis: Dict[str, Any],
                                         image_placement_plan: Dict[str, Any] = None) -> str:
        """
        플랫폼별 특화 프롬프트 생성
        """
        platform_spec = self.platform_specs.get(request.platform, self.platform_specs['인스타그램'])
        tone_style = self.tone_styles.get(request.toneAndManner, {}).get(request.platform, '친근하고 자연스러운 어조')

        # 이미지 설명 추출
        image_descriptions = []
        for result in image_analysis.get('results', []):
            if 'description' in result:
                image_descriptions.append(result['description'])

        # 플랫폼별 특화 프롬프트 생성
        if request.platform == '인스타그램':
            return self._create_instagram_prompt(request, platform_spec, tone_style, image_descriptions)
        elif request.platform == '네이버 블로그':
            return self._create_naver_blog_prompt(request, platform_spec, tone_style, image_descriptions,
                                                  image_placement_plan)
        else:
            return self._create_instagram_prompt(request, platform_spec, tone_style, image_descriptions)

    def _create_instagram_prompt(self, request: SnsContentGetRequest, platform_spec: dict, tone_style: str,
                                 image_descriptions: list) -> str:
        """
        인스타그램 특화 프롬프트
        """
        category_hashtags = self.category_keywords.get(request.category, {}).get('인스타그램', [])

        prompt = f"""
당신은 인스타그램 마케팅 전문가입니다. 소상공인 음식점을 위한 매력적인 인스타그램 게시물을 작성해주세요.

**🎯 콘텐츠 정보:**
- 제목: {request.title}
- 카테고리: {request.category}
- 콘텐츠 타입: {request.contentType}
- 메뉴명: {request.menuName or '특별 메뉴'}
- 이벤트: {request.eventName or '특별 이벤트'}

**📱 인스타그램 특화 요구사항:**
- 글 구조: {platform_spec['content_structure']}
- 최대 길이: {platform_spec['max_length']}자
- 해시태그: {platform_spec['hashtag_count']}개 내외
- 톤앤매너: {tone_style}

**✨ 인스타그램 작성 가이드라인:**
{chr(10).join([f"- {tip}" for tip in platform_spec['writing_tips']])}

**📸 이미지 분석 결과:**
{chr(10).join(image_descriptions) if image_descriptions else '시각적으로 매력적인 음식/매장 이미지'}

**🏷️ 추천 해시태그 카테고리:**
- 기본 해시태그: {', '.join(category_hashtags[:5])}
- 브랜딩: #우리가게이름 (실제 가게명으로 대체)
- 지역: #강남맛집 #서울카페 (실제 위치로 대체)
- 감정: #행복한시간 #맛있다 #추천해요

**💡 콘텐츠 작성 지침:**
1. 첫 문장은 반드시 관심을 끄는 후킹 문장으로 시작
2. 이모티콘을 적절히 활용하여 시각적 재미 추가
3. 스토리텔링을 통해 감정적 연결 유도
4. 명확한 행동 유도 문구 포함 (팔로우, 댓글, 저장, 방문 등)
5. 줄바꿈을 활용하여 가독성 향상
6. 해시태그는 본문과 자연스럽게 연결되도록 배치

**특별 요구사항:**
{request.requirement or '고객의 관심을 끌고 방문을 유도하는 매력적인 게시물'}

인스타그램 사용자들이 "저장하고 싶다", "친구에게 공유하고 싶다"라고 생각할 만한 매력적인 게시물을 작성해주세요.
"""
        return prompt

    def _create_naver_blog_prompt(self, request: SnsContentGetRequest, platform_spec: dict, tone_style: str,
                                  image_descriptions: list, image_placement_plan: Dict[str, Any]) -> str:
        """
        네이버 블로그 특화 프롬프트 (이미지 배치 계획 포함)
        """
        category_keywords = self.category_keywords.get(request.category, {}).get('네이버 블로그', [])
        seo_keywords = platform_spec['seo_keywords']

        # 이미지 배치 정보 추가
        image_placement_info = ""
        if image_placement_plan:
            image_placement_info = f"""

**📸 이미지 배치 계획:**
{chr(10).join([f"- {section['section']}: {section['placement_guide']}" for section in image_placement_plan['structure']])}

**이미지 사용 순서:**
{chr(10).join([f"{i + 1}. {img.get('description', 'Image')} (타입: {img.get('type', '기타')})" for i, img in enumerate(image_placement_plan.get('image_sequence', []))])}
"""

        prompt = f"""
당신은 네이버 블로그 맛집 리뷰 전문가입니다. 검색 최적화와 정보 제공을 중시하는 네이버 블로그 특성에 맞는 게시물을 작성해주세요.

**📝 콘텐츠 정보:**
- 제목: {request.title}
- 카테고리: {request.category}
- 콘텐츠 타입: {request.contentType}
- 메뉴명: {request.menuName or '대표 메뉴'}
- 이벤트: {request.eventName or '특별 이벤트'}

**🔍 네이버 블로그 특화 요구사항:**
- 글 구조: {platform_spec['content_structure']}
- 최대 길이: {platform_spec['max_length']}자
- 톤앤매너: {tone_style}
- SEO 최적화 필수

**📚 블로그 작성 가이드라인:**
{chr(10).join([f"- {tip}" for tip in platform_spec['writing_tips']])}

**🖼️ 이미지 분석 결과:**
{chr(10).join(image_descriptions) if image_descriptions else '상세한 음식/매장 정보'}

{image_placement_info}

**🔑 SEO 키워드 (자연스럽게 포함할 것):**
- 필수 키워드: {', '.join(seo_keywords[:8])}
- 카테고리 키워드: {', '.join(category_keywords[:5])}

**📖 블로그 포스트 구조 (이미지 배치 포함):**
1. **인트로**: 방문 동기와 첫인상 + [IMAGE_1] 배치
2. **매장 정보**: 위치, 운영시간, 분위기 + [IMAGE_2, IMAGE_3] 배치  
3. **메뉴 소개**: 주문한 메뉴와 상세 후기 + [IMAGE_4, IMAGE_5] 배치
4. **총평**: 재방문 의향과 추천 이유 + [IMAGE_6] 배치

**💡 콘텐츠 작성 지침:**
1. 검색자의 궁금증을 해결하는 정보 중심 작성
2. 구체적인 가격, 위치, 운영시간 등 실용 정보 포함
3. 개인적인 경험과 솔직한 후기 작성
4. 각 섹션마다 적절한 위치에 [IMAGE_X] 태그로 이미지 배치 위치 표시
5. 이미지마다 간단한 설명 문구 추가
6. 지역 정보와 접근성 정보 포함

**이미지 태그 사용법:**
- [IMAGE_1]: 첫 번째 이미지 배치 위치
- [IMAGE_2]: 두 번째 이미지 배치 위치  
- 각 이미지 태그 다음 줄에 이미지 설명 문구 작성

**특별 요구사항:**
{request.requirement or '유용한 정보를 제공하여 방문을 유도하는 신뢰성 있는 후기'}

네이버 검색에서 상위 노출되고, 실제로 도움이 되는 정보를 제공하는 블로그 포스트를 작성해주세요.
이미지 배치 위치를 [IMAGE_X] 태그로 명확히 표시해주세요.
"""
        return prompt

    def _post_process_content(self, content: str, request: SnsContentGetRequest) -> str:
        """
        플랫폼별 후처리
        """
        if request.platform == '인스타그램':
            return self._post_process_instagram(content, request)
        elif request.platform == '네이버 블로그':
            return self._post_process_naver_blog(content, request)
        return content

    def _post_process_instagram(self, content: str, request: SnsContentGetRequest) -> str:
        """
        인스타그램 콘텐츠 후처리
        """
        import re

        # 해시태그 개수 조정
        hashtags = re.findall(r'#[\w가-힣]+', content)
        if len(hashtags) > 15:
            # 해시태그가 너무 많으면 중요도 순으로 15개만 유지
            all_hashtags = ' '.join(hashtags[:15])
            content = re.sub(r'#[\w가-힣]+', '', content)
            content = content.strip() + '\n\n' + all_hashtags

        # 이모티콘이 부족하면 추가
        emoji_count = content.count('😊') + content.count('🍽️') + content.count('❤️') + content.count('✨')
        if emoji_count < 3:
            content = content.replace('!', '! 😊', 1)

        return content

    def _post_process_naver_blog(self, content: str, request: SnsContentGetRequest) -> str:
        """
        네이버 블로그 콘텐츠 후처리
        """
        # 구조화된 형태로 재구성
        if '📍' not in content and '🏷️' not in content:
            # 이모티콘 기반 구조화가 없으면 추가
            lines = content.split('\n')
            structured_content = []
            for line in lines:
                if '위치' in line or '주소' in line:
                    line = f"📍 {line}"
                elif '가격' in line or '메뉴' in line:
                    line = f"🏷️ {line}"
                elif '분위기' in line or '인테리어' in line:
                    line = f"🏠 {line}"
                structured_content.append(line)
            content = '\n'.join(structured_content)

        return content

    def _format_to_html(self, content: str, request: SnsContentGetRequest,
                        image_placement_plan: Dict[str, Any] = None) -> str:
        """
        생성된 콘텐츠를 HTML 형식으로 포맷팅 (이미지 배치 포함)
        """
        # 1. literal \n 문자열을 실제 줄바꿈으로 변환
        content = content.replace('\\n', '\n')

        # 2. 네이버 블로그인 경우 이미지 태그를 실제 이미지로 변환
        if request.platform == '네이버 블로그' and image_placement_plan:
            content = self._replace_image_tags_with_html(content, image_placement_plan, request.images)

        # 3. 실제 줄바꿈을 <br> 태그로 변환
        content = content.replace('\n', '<br>')

        # 4. 추가 정리: \r, 여러 공백 정리
        content = content.replace('\\r', '').replace('\r', '')

        # 5. 여러 개의 <br> 태그를 하나로 정리
        import re
        content = re.sub(r'(<br>\s*){3,}', '<br><br>', content)

        # 6. 해시태그를 파란색으로 스타일링
        content = re.sub(r'(#[\w가-힣]+)', r'<span style="color: #1DA1F2; font-weight: bold;">\1</span>', content)

        # 플랫폼별 헤더 스타일
        platform_style = ""
        if request.platform == '인스타그램':
            platform_style = "background: linear-gradient(45deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%);"
        elif request.platform == '네이버 블로그':
            platform_style = "background: linear-gradient(135deg, #1EC800 0%, #00B33C 100%);"
        else:
            platform_style = "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);"

        # 전체 HTML 구조
        html_content = f"""
           <div style="font-family: 'Noto Sans KR', Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 600px;">
               <div style="{platform_style} color: white; padding: 15px; border-radius: 10px 10px 0 0; text-align: center;">
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

    def _replace_image_tags_with_html(self, content: str, image_placement_plan: Dict[str, Any],
                                      image_urls: List[str]) -> str:
        """
        네이버 블로그 콘텐츠의 [IMAGE_X] 태그를 실제 이미지 HTML로 변환
        """
        import re

        # [IMAGE_X] 패턴 찾기
        image_tags = re.findall(r'\[IMAGE_(\d+)\]', content)

        for tag in image_tags:
            image_index = int(tag) - 1  # 1-based to 0-based

            if image_index < len(image_urls):
                image_url = image_urls[image_index]

                # 이미지 배치 계획에서 해당 이미지 정보 찾기
                image_info = None
                for img in image_placement_plan.get('image_sequence', []):
                    if img.get('index') == image_index:
                        image_info = img
                        break

                # 이미지 설명 생성
                image_description = ""
                if image_info:
                    description = image_info.get('description', '')
                    img_type = image_info.get('type', '기타')

                    if img_type == '음식':
                        image_description = f"😋 {description}"
                    elif img_type == '매장외관':
                        image_description = f"🏪 {description}"
                    elif img_type == '인테리어':
                        image_description = f"🏠 {description}"
                    elif img_type == '메뉴판':
                        image_description = f"📋 {description}"
                    else:
                        image_description = f"📸 {description}"

                # HTML 이미지 태그로 변환
                image_html = f"""
        <div style="text-align: center; margin: 20px 0;">
           <img src="{image_url}" alt="이미지" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
           <div style="font-size: 14px; color: #666; margin-top: 8px; font-style: italic;">
               {image_description}
           </div>
        </div>"""

                # 콘텐츠에서 태그 교체
                content = content.replace(f'[IMAGE_{tag}]', image_html)

        return content

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
        metadata_html += f'<div><strong>플랫폼:</strong> {request.platform}</div>'
        metadata_html += f'<div><strong>생성일:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>'
        metadata_html += '</div>'

        return metadata_html
