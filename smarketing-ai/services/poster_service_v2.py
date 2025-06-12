"""
하이브리드 포스터 생성 서비스
DALL-E: 텍스트 없는 아름다운 배경 생성
PIL: 완벽한 한글 텍스트 오버레이
"""
import os
from typing import Dict, Any
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import requests
import io
from utils.ai_client import AIClient
from utils.image_processor import ImageProcessor
from models.request_models import PosterContentGetRequest


class PosterServiceV2:
    """하이브리드 포스터 생성 서비스"""

    def __init__(self):
        """서비스 초기화"""
        self.ai_client = AIClient()
        self.image_processor = ImageProcessor()

    def generate_poster(self, request: PosterContentGetRequest) -> Dict[str, Any]:
        """
        하이브리드 포스터 생성
        1. DALL-E로 텍스트 없는 배경 생성
        2. PIL로 완벽한 한글 텍스트 오버레이
        """
        try:
            # 1. 참조 이미지 분석
            image_analysis = self._analyze_reference_images(request.images)

            # 2. DALL-E로 텍스트 없는 배경 생성
            background_prompt = self._create_background_only_prompt(request, image_analysis)
            background_url = self.ai_client.generate_image_with_openai(background_prompt, "1024x1024")

            # 3. 배경 이미지 다운로드
            background_image = self._download_and_load_image(background_url)

            # 4. AI로 텍스트 컨텐츠 생성
            text_content = self._generate_text_content(request)

            # 5. PIL로 한글 텍스트 오버레이
            final_poster = self._add_perfect_korean_text(background_image, text_content, request)

            # 6. 최종 이미지 저장
            poster_url = self._save_final_poster(final_poster)

            return {
                'success': True,
                'content': poster_url
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _create_background_only_prompt(self, request: PosterContentGetRequest, image_analysis: Dict[str, Any]) -> str:
        """텍스트 완전 제외 배경 전용 프롬프트"""

        # 참조 이미지 설명
        reference_descriptions = []
        for result in image_analysis.get('results', []):
            if 'description' in result:
                reference_descriptions.append(result['description'])

        prompt = f"""
Create a beautiful text-free background design for a Korean restaurant promotional poster.

ABSOLUTE REQUIREMENTS:
- NO TEXT, NO LETTERS, NO WORDS, NO CHARACTERS of any kind
- Pure visual background design only
- Professional Korean food business aesthetic
- Leave clear areas for text overlay (top 20% and bottom 30%)

DESIGN STYLE:
- Category: {request.category} themed design
- Photo Style: {request.photoStyle or 'modern'} aesthetic
- Mood: {request.toneAndManner or 'friendly'} atmosphere
- Intensity: {request.emotionIntensity or 'medium'} visual impact

VISUAL ELEMENTS TO INCLUDE:
- Korean traditional patterns or modern geometric designs
- Food-related visual elements (ingredients, cooking utensils, abstract food shapes)
- Warm, appetizing color palette
- Professional restaurant branding feel
- Clean, modern layout structure

REFERENCE CONTEXT:
{chr(10).join(reference_descriptions) if reference_descriptions else 'Clean, professional food business design'}

COMPOSITION:
- Central visual focus area
- Clear top section for main title
- Clear bottom section for details
- Balanced negative space
- High-end restaurant poster aesthetic

STRICTLY AVOID:
- Any form of text (Korean, English, numbers, symbols)
- Menu boards or signs with text
- Price displays
- Written content of any kind
- Typography elements

Create a premium, appetizing background that will make customers want to visit the restaurant.
Focus on visual appeal, color harmony, and professional food business branding.
"""
        return prompt

    def _download_and_load_image(self, image_url: str) -> Image.Image:
        """이미지 URL에서 PIL 이미지로 로드"""
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content))

    def _generate_text_content(self, request: PosterContentGetRequest) -> Dict[str, str]:
        """AI로 포스터 텍스트 컨텐츠 생성"""
        prompt = f"""
한국 음식점 홍보 포스터용 텍스트를 생성해주세요.

포스터 정보:
- 제목: {request.title}
- 카테고리: {request.category}
- 메뉴명: {request.menuName or ''}
- 이벤트명: {request.eventName or ''}
- 시작일: {request.startDate or ''}
- 종료일: {request.endDate or ''}

다음 형식으로만 답변해주세요:
메인제목: [임팩트 있는 제목 8자 이내]
서브제목: [설명 문구 15자 이내]
기간정보: [기간 표시]
액션문구: [행동유도 8자 이내]
"""

        try:
            ai_response = self.ai_client.generate_text(prompt, max_tokens=150)
            return self._parse_text_content(ai_response, request)
        except:
            return self._create_fallback_content(request)

    def _parse_text_content(self, ai_response: str, request: PosterContentGetRequest) -> Dict[str, str]:
        """AI 응답 파싱"""
        content = {
            'main_title': request.title[:8],
            'sub_title': '',
            'period_info': '',
            'action_text': '지금 확인!'
        }

        lines = ai_response.split('\n')
        for line in lines:
            line = line.strip()
            if '메인제목:' in line:
                content['main_title'] = line.split('메인제목:')[1].strip()
            elif '서브제목:' in line:
                content['sub_title'] = line.split('서브제목:')[1].strip()
            elif '기간정보:' in line:
                content['period_info'] = line.split('기간정보:')[1].strip()
            elif '액션문구:' in line:
                content['action_text'] = line.split('액션문구:')[1].strip()

        return content

    def _create_fallback_content(self, request: PosterContentGetRequest) -> Dict[str, str]:
        """AI 실패시 기본 컨텐츠"""
        return {
            'main_title': request.title[:8] if request.title else '특별 이벤트',
            'sub_title': request.eventName or request.menuName or '맛있는 음식',
            'period_info': f"{request.startDate} ~ {request.endDate}" if request.startDate and request.endDate else '',
            'action_text': '지금 방문!'
        }

    def _add_perfect_korean_text(self, background: Image.Image, content: Dict[str, str], request: PosterContentGetRequest) -> Image.Image:
        """완벽한 한글 텍스트 오버레이"""

        # 배경 이미지 복사
        poster = background.copy()
        draw = ImageDraw.Draw(poster)
        width, height = poster.size

        # 한글 폰트 로드 (여러 경로 시도)
        fonts = self._load_korean_fonts()

        # 텍스트 색상 결정 (배경 분석 기반)
        text_color = self._determine_text_color(background)
        shadow_color = (0, 0, 0) if text_color == (255, 255, 255) else (255, 255, 255)

        # 1. 메인 제목 (상단)
        if content['main_title']:
            self._draw_text_with_effects(
                draw, content['main_title'],
                fonts['title'], text_color, shadow_color,
                width // 2, height * 0.15, 'center'
            )

        # 2. 서브 제목
        if content['sub_title']:
            self._draw_text_with_effects(
                draw, content['sub_title'],
                fonts['subtitle'], text_color, shadow_color,
                width // 2, height * 0.75, 'center'
            )

        # 3. 기간 정보
        if content['period_info']:
            self._draw_text_with_effects(
                draw, content['period_info'],
                fonts['small'], text_color, shadow_color,
                width // 2, height * 0.82, 'center'
            )

        # 4. 액션 문구 (강조 배경)
        if content['action_text']:
            self._draw_call_to_action(
                draw, content['action_text'],
                fonts['subtitle'], width, height
            )

        return poster

    def _load_korean_fonts(self) -> Dict[str, ImageFont.FreeTypeFont]:
        """한글 폰트 로드 (여러 경로 시도)"""
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Arial.ttf",  # macOS
            "C:/Windows/Fonts/arial.ttf",       # Windows
            "/usr/share/fonts/TTF/arial.ttf"    # Linux
        ]

        fonts = {}

        for font_path in font_paths:
            try:
                fonts['title'] = ImageFont.truetype(font_path, 60)
                fonts['subtitle'] = ImageFont.truetype(font_path, 32)
                fonts['small'] = ImageFont.truetype(font_path, 24)
                break
            except:
                continue

        # 폰트 로드 실패시 기본 폰트
        if not fonts:
            fonts = {
                'title': ImageFont.load_default(),
                'subtitle': ImageFont.load_default(),
                'small': ImageFont.load_default()
            }

        return fonts

    def _determine_text_color(self, image: Image.Image) -> tuple:
        """배경 이미지 분석하여 텍스트 색상 결정"""
        # 이미지 상단과 하단의 평균 밝기 계산
        top_region = image.crop((0, 0, image.width, image.height // 4))
        bottom_region = image.crop((0, image.height * 3 // 4, image.width, image.height))

        def get_brightness(img_region):
            grayscale = img_region.convert('L')
            pixels = list(grayscale.getdata())
            return sum(pixels) / len(pixels)

        top_brightness = get_brightness(top_region)
        bottom_brightness = get_brightness(bottom_region)
        avg_brightness = (top_brightness + bottom_brightness) / 2

        # 밝으면 검은색, 어두우면 흰색 텍스트
        return (50, 50, 50) if avg_brightness > 128 else (255, 255, 255)

    def _draw_text_with_effects(self, draw, text, font, color, shadow_color, x, y, align='center'):
        """그림자 효과가 있는 텍스트 그리기"""
        if not text:
            return

        # 텍스트 크기 계산
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # 위치 조정
        if align == 'center':
            x = x - text_width // 2

        # 배경 박스 (가독성 향상)
        padding = 10
        box_coords = [
            x - padding, y - padding,
            x + text_width + padding, y + text_height + padding
        ]
        draw.rectangle(box_coords, fill=(0, 0, 0, 180))

        # 그림자 효과
        shadow_offset = 2
        draw.text((x + shadow_offset, y + shadow_offset), text, fill=shadow_color, font=font)

        # 메인 텍스트
        draw.text((x, y), text, fill=color, font=font)

    def _draw_call_to_action(self, draw, text, font, width, height):
        """강조된 액션 버튼 스타일 텍스트"""
        if not text:
            return

        # 버튼 위치 (하단 중앙)
        button_y = height * 0.88

        # 텍스트 크기
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # 버튼 배경
        button_width = text_width + 40
        button_height = text_height + 20
        button_x = (width - button_width) // 2

        # 버튼 그리기
        button_coords = [
            button_x, button_y - 10,
            button_x + button_width, button_y + button_height
        ]
        draw.rounded_rectangle(button_coords, radius=25, fill=(255, 107, 107))

        # 텍스트 그리기
        text_x = (width - text_width) // 2
        text_y = button_y + 5
        draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)

    def _save_final_poster(self, poster: Image.Image) -> str:
        """최종 포스터 저장"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"hybrid_poster_{timestamp}.png"
        filepath = os.path.join('uploads', 'temp', filename)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        poster.save(filepath, 'PNG', quality=95)

        return f"http://localhost:5001/uploads/temp/{filename}"

    def _analyze_reference_images(self, image_urls: list) -> Dict[str, Any]:
        """참조 이미지 분석 (기존 코드와 동일)"""
        if not image_urls:
            return {'total_images': 0, 'results': []}

        analysis_results = []
        temp_files = []

        try:
            for image_url in image_urls:
                temp_path = self.ai_client.download_image_from_url(image_url)
                if temp_path:
                    temp_files.append(temp_path)
                    try:
                        image_description = self.ai_client.analyze_image(temp_path)
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
            for temp_file in temp_files:
                try:
                    os.remove(temp_file)
                except:
                    pass