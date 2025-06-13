"""
포스터 생성 서비스 V3
OpenAI DALL-E를 사용한 이미지 생성 (메인 메뉴 이미지 1개 + 프롬프트 내 예시 링크 10개)
"""
import os
from typing import Dict, Any, List
from datetime import datetime
from utils.ai_client import AIClient
from utils.image_processor import ImageProcessor
from models.request_models import PosterContentGetRequest


class PosterServiceV3:
    """포스터 생성 서비스 V3 클래스"""

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
            '이벤트': '홍보용 디자인, 눈길을 끄는',
            '메뉴': '메뉴 디자인, 정리된 레이아웃',
            '할인': '세일 포스터, 할인 디자인',
            '음료': '시원하고 상쾌한, 맛있어 보이는 음료'
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
        포스터 생성 (메인 이미지 1개 분석 + 예시 링크 10개 프롬프트 제공)
        """
        try:
            # 메인 이미지 확인
            if not request.images:
                return {'success': False, 'error': '메인 메뉴 이미지가 제공되지 않았습니다.'}

            main_image_url = request.images[0]  # 첫 번째 이미지가 메인 메뉴

            # 메인 이미지 분석
            main_image_analysis = self._analyze_main_image(main_image_url)

            # 포스터 생성 프롬프트 생성 (예시 링크 10개 포함)
            prompt = self._create_poster_prompt_v3(request, main_image_analysis)

            # OpenAI로 이미지 생성
            image_url = self.ai_client.generate_image_with_openai(prompt, "1024x1024")

            return {
                'success': True,
                'content': image_url,
                'analysis': {
                    'main_image': main_image_analysis,
                    'example_images_used': len(self.example_images)
                }
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _analyze_main_image(self, image_url: str) -> Dict[str, Any]:
        """
        메인 메뉴 이미지 분석
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
        finally:
            # 임시 파일 정리
            for temp_file in temp_files:
                try:
                    os.remove(temp_file)
                except:
                    pass

    def _create_poster_prompt_v3(self, request: PosterContentGetRequest,
                                 main_analysis: Dict[str, Any]) -> str:
        """
        V3 포스터 생성을 위한 AI 프롬프트 생성 (한글, 글자 완전 제외, 메인 이미지 기반 + 예시 링크 10개 포함)
        """
        # 기본 스타일 설정
        photo_style = self.photo_styles.get(request.photoStyle, '현대적이고 깔끔한 디자인')
        category_style = self.category_styles.get(request.category, '홍보용 디자인')
        tone_style = self.tone_styles.get(request.toneAndManner, '친근하고 따뜻한 느낌')
        emotion_design = self.emotion_designs.get(request.emotionIntensity, '적당히 활기찬 디자인')

        # 메인 이미지 정보 활용
        main_description = main_analysis.get('description', '맛있는 음식')
        main_colors = main_analysis.get('dominant_colors', [])
        main_image_url = main_analysis.get('url', '')
        image_info = main_analysis.get('info', {})
        is_food = main_analysis.get('is_food', False)

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
                메인 이미지 URL을 참조하여, "글이 없는" 심플한 카페 포스터를 디자인해주세요.

                **핵심 기준 이미지:**
                메인 이미지 URL: {main_image_url}
                이 이미지 URL에 들어가 이미지를 다운로드 후, 이 이미지를 그대로 반영한 채 홍보 포스터를 디자인해주세요.
                심플한 배경이 중요합니다.
                AI가 생성하지 않은 것처럼 현실적인 요소를 반영해주세요.

                **절대 필수 조건:**
                - 어떤 형태의 텍스트, 글자, 문자, 숫자도 절대 포함하지 말 것!!!! - 가장 중요
                - 위의 메인 이미지를 임의 변경 없이, 포스터의 중심 요소로 포함할 것
                - 하나의 포스터만 생성해주세요
                - 메인 이미지의 색감과 분위기를 살려서 심플한 포스터 디자인
                - 메인 이미지가 돋보이도록 배경과 레이아웃 구성
                - 확실하지도 않은 문자 절대 생성 x

                **특별 요구사항:**
                {request.requirement}



                **반드시 제외할 요소:**
                - 모든 형태의 텍스트 (한글, 영어, 숫자, 기호)
                - 메뉴판, 가격표, 간판
                - 글자가 적힌 모든 요소
                - 브랜드 로고나 문자

                """
        return prompt
