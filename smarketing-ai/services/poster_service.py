"""
포스터 생성 서비스 V3
OpenAI DALL-E를 사용한 이미지 생성 (메인 메뉴 이미지 1개 + 프롬프트 내 예시 링크 10개)
"""
import os
from typing import Dict, Any, List
from utils.ai_client import AIClient
from utils.image_processor import ImageProcessor
from models.request_models import PosterContentGetRequest


class PosterService:

    def __init__(self):
        """서비스 초기화"""
        self.ai_client = AIClient()
        self.image_processor = ImageProcessor()

        # Azure Blob Storage 예시 이미지 링크 10개 (카페 음료 관련)
        self.example_images = [
            "https://stdigitalgarage02.blob.core.windows.net/ai-content/example1.png",
            "https://stdigitalgarage02.blob.core.windows.net/ai-content/example2.png",
            "https://stdigitalgarage02.blob.core.windows.net/ai-content/example3.png",
            "https://stdigitalgarage02.blob.core.windows.net/ai-content/example4.png",
            "https://stdigitalgarage02.blob.core.windows.net/ai-content/example5.png",
            "https://stdigitalgarage02.blob.core.windows.net/ai-content/example6.png",
            "https://stdigitalgarage02.blob.core.windows.net/ai-content/example7.png"
        ]

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
            '이벤트': '홍보용 디자인, 눈길을 끄는'
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
        포스터 생성 (메인 이미지 1개 분석 + 예시 링크 7개 프롬프트 제공)
        """
        try:
            # 메인 이미지 확인
            if not request.images:
                return {'success': False, 'error': '메인 메뉴 이미지가 제공되지 않았습니다.'}

            main_image_url = request.images[0]  # 첫 번째 이미지가 메인 메뉴

            # 메인 이미지 분석
            main_image_analysis = self._analyze_main_image(main_image_url)

            # 포스터 생성 프롬프트 생성
            prompt = self._create_poster_prompt(request, main_image_analysis)

            # OpenAI로 이미지 생성
            image_url = self.ai_client.generate_image_with_openai(prompt, "1024x1536")

            return {
                'success': True,
                'content': image_url,
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _analyze_main_image(self, image_url: str) -> Dict[str, Any]:
        """
        메인 메뉴 이미지 분석 시작
        """
        temp_files = []
        try:
            # 이미지 다운로드
            temp_path = self.ai_client.download_image_from_url(image_url)
            if temp_path:
                temp_files.append(temp_path)

                # 이미지 분석
                image_info = self.image_processor.get_image_info(temp_path)
                image_description = self.ai_client.analyze_image(temp_path)
                colors = self.image_processor.analyze_colors(temp_path, 5)

                return {
                    'url': image_url,
                    'info': image_info,
                    'description': image_description,
                    'dominant_colors': colors,
                    'is_food': self.image_processor.is_food_image(temp_path)
                }
            else:
                return {
                    'url': image_url,
                    'error': '이미지 다운로드 실패'
                }

        except Exception as e:
            return {
                'url': image_url,
                'error': str(e)
            }

    def _create_poster_prompt(self, request: PosterContentGetRequest,
                              main_analysis: Dict[str, Any]) -> str:
        """
        카테고리에 따른 포스터 생성 프롬프트 분기
        """
        if request.category == "음식":
            return self._create_food_poster_prompt(request, main_analysis)
        elif request.category == "이벤트":
            return self._create_event_poster_prompt(request, main_analysis)
        else:
            # 기본값으로 음식 프롬프트 사용
            return self._create_food_poster_prompt(request, main_analysis)

    def _create_food_poster_prompt(self, request: PosterContentGetRequest,
                                   main_analysis: Dict[str, Any]) -> str:
        """
        포스터 생성을 위한 AI 프롬프트 생성 (한글, 글자 완전 제외, 메인 이미지 기반 + 예시 링크 7개 포함)
        """

        # 메인 이미지 정보 활용
        main_image = main_analysis.get('url')
        main_description = main_analysis.get('description', '맛있는 음식')
        main_colors = main_analysis.get('dominant_colors', [])
        image_info = main_analysis.get('info', {})

        # 이미지 크기 및 비율 정보
        aspect_ratio = image_info.get('aspect_ratio', 1.0) if image_info else 1.0
        image_orientation = "가로형" if aspect_ratio > 1.2 else "세로형" if aspect_ratio < 0.8 else "정사각형"

        # 색상 정보를 텍스트로 변환
        color_description = ""
        if main_colors:
            color_rgb = main_colors[:3]  # 상위 3개 색상
            color_description = f"주요 색상 RGB 값: {color_rgb}를 기반으로 한 조화로운 색감"

        # 예시 이미지 링크들을 문자열로 변환
        example_links = "\n".join([f"- {link}" for link in self.example_images])

        prompt = f"""
        ## {main_image}를 활용한 홍보 포스터 디자인 요청
        
        ### 📋 기본 정보
        메뉴 이미지 : {main_image}
        메뉴명: {request.menuName or '없음'}
        메뉴 정보: {main_description}
        
        ### 🎨 디자인 요구사항
        메인 이미지 처리
        - {main_image}는 변경 없이 그대로 사용해주세요.
        - 기존 메인 이미지는 변경하지 않고 그대로 유지
        - 포스터 전체 크기의 1/3 이하로 배치
        - 이미지와 조화로운 작은 장식 이미지 추가
        - 크기: {image_orientation}
        
        텍스트 요소
        - 메뉴명 (필수)
        - 간단한 추가 홍보 문구 (새로 생성, 한글) 혹은 "{request.requirement or '눈길을 끄는 전문적인 디자인'}"라는 요구사항에 맞는 문구
        - 메뉴명 외 추가되는 문구는 1줄만 작성
        
        
        텍스트 배치 규칙
        - 글자가 이미지 경계를 벗어나지 않도록 주의
        - 모서리에 너무 가깝게 배치하지 말 것
        - 적당한 크기로 가독성 확보
        - 아기자기한 한글 폰트 사용
        
        ### 🎨 디자인 스타일
        참조 이미지
        {example_links}의 URL을 참고하여 비슷한 스타일로 제작
        
        색상 가이드
        {color_description}
        전체적인 디자인 방향
        
        타겟: 한국 카페 고객층
        스타일: 화려하고 매력적인 디자인
        목적: 소셜미디어 공유용 (적합한 크기)
        톤앤매너: 맛있어 보이는 색상, 방문 유도하는 비주얼
        
        ### 🎯 최종 목표
        고객들이 이 음식을 먹고싶다 생각하게 만드는 시각적으로 매력적인 홍보 포스터 제작
        """

        return prompt


    def _create_event_poster_prompt(self, request: PosterContentGetRequest,
                                    main_analysis: Dict[str, Any]) -> str:
        """
        이벤트 카테고리 포스터 생성을 위한 AI 프롬프트 생성
        """
        # 메인 이미지 정보 활용
        main_image = main_analysis.get('url')
        main_description = main_analysis.get('description', '특별 이벤트')
        main_colors = main_analysis.get('dominant_colors', [])
        image_info = main_analysis.get('info', {})

        # 이미지 크기 및 비율 정보
        aspect_ratio = image_info.get('aspect_ratio', 1.0) if image_info else 1.0
        image_orientation = "가로형" if aspect_ratio > 1.2 else "세로형" if aspect_ratio < 0.8 else "정사각형"

        # 색상 정보를 텍스트로 변환
        color_description = ""
        if main_colors:
            color_rgb = main_colors[:3]  # 상위 3개 색상
            color_description = f"주요 색상 RGB 값: {color_rgb}를 기반으로 한 임팩트 있는 색감"

        # 예시 이미지 링크들을 문자열로 변환
        example_links = "\n".join([f"- {link}" for link in self.example_images])

        prompt = f"""
            ## {main_image}를 활용한 이벤트 홍보 포스터 디자인 요청
            메인 이미지에서 최대한 배경만 변경하는 식으로 활용하기
            
    
            ### 📋 기본 정보
            이벤트 이미지 : {main_image}
            메뉴명: {request.menuName or '없음'}
            이벤트명: {request.requirement or '특별 이벤트'} {request.requirement}가 이벤트와 관련이 있다면 활용
            이벤트 정보: {main_description}
    
            ### 📅 이벤트 기간 (중요!)
            시작일: {request.startDate or '지금'}
            종료일: {request.endDate or '한정 기간'}
            ⚠️ 이벤트 기간은 가장 눈에 띄게 크고 강조하여 표시해주세요!
    
            ### 🎨 이벤트 특화 디자인 요구사항
            메인 이미지 처리
            - {main_image}는 변경 없이 그대로 사용해주세요.
            - AI가 그린 것 같지 않은, 현실적인 사진으로 사용
            - 이벤트의 핵심 내용을 시각적으로 강조
            - 포스터 전체 크기의 30% 영역에 배치 (텍스트 공간 확보)
            - 이벤트 분위기에 맞는 역동적인 배치
            - 크기: {image_orientation}
    
            텍스트 요소 (이벤트 전용)
            - 이벤트명을 가장 크고 임팩트 있게 표시
            - 둥글둥글한 폰트 활용
            - 이벤트 기간을 박스나 강조 영역으로 처리
            - 메뉴명과 이벤트명만 기입해주고 나머지 텍스트는 기입하지 않음.
            - 한글로 작성 필수이고, 절대 한글이 깨지지 않게 만들어주세요. 만약 깨질 것 같다면 그냥 빼주세요.
    
            이벤트 포스터만의 특별 요소
            - 이미지에 맞는 임팩트 및 패턴 강조
            - 할인이나 혜택을 강조하는 스티커 효과    
    
            색상 가이드
            - {color_description}과 비슷한 톤으로 생성
            
    
            ### 🎯 최종 목표
            고객들이 "지금 당장 가서 이 이벤트에 참여해야겠다!"라고 생각하게 만드는 강렬하고 화려한 이벤트 홍보 포스터 제작
            """

        return prompt
