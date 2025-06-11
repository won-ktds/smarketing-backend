"""
홍보 포스터 생성 서비스
AI와 이미지 처리를 활용한 시각적 마케팅 자료 생성
"""
import os
import base64
from typing import Dict, Any
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from utils.ai_client import AIClient
from utils.image_processor import ImageProcessor
from models.request_models import PosterRequest
class PosterService:
    """홍보 포스터 생성 서비스 클래스"""
    def __init__(self):
        """서비스 초기화"""
        self.ai_client = AIClient()
        self.image_processor = ImageProcessor()
        # 포스터 기본 설정
        self.poster_config = {
            'width': 1080,
            'height': 1350,  # 인스타그램 세로 비율
            'background_color': (255, 255, 255),
            'text_color': (50, 50, 50),
            'accent_color': (255, 107, 107)
        }
        # 카테고리별 색상 테마
        self.category_themes = {
            '음식': {
                'primary': (255, 107, 107),    # 빨강
                'secondary': (255, 206, 84),   # 노랑
                'background': (255, 248, 240)  # 크림
            },
            '매장': {
                'primary': (74, 144, 226),     # 파랑
                'secondary': (120, 198, 121),  # 초록
                'background': (248, 251, 255)  # 연한 파랑
            },
            '이벤트': {
                'primary': (156, 39, 176),     # 보라
                'secondary': (255, 193, 7),    # 금색
                'background': (252, 248, 255)  # 연한 보라
            }
        }
    def generate_poster(self, request: PosterRequest) -> Dict[str, Any]:
        """
        홍보 포스터 생성
        Args:
            request: 포스터 생성 요청 데이터
        Returns:
            생성된 포스터 정보
        """
        try:
            # 포스터 텍스트 내용 생성
            poster_text = self._generate_poster_text(request)
            # 이미지 전처리
            processed_images = self._process_images(request.image_paths)
            # 포스터 이미지 생성
            poster_image = self._create_poster_image(request, poster_text, processed_images)
            # 이미지를 base64로 인코딩
            poster_base64 = self._encode_image_to_base64(poster_image)
            return {
                'success': True,
                'poster_data': poster_base64,
                'poster_text': poster_text,
                'category': request.category,
                'generated_at': datetime.now().isoformat(),
                'image_count': len(request.image_paths),
                'format': 'base64'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'generated_at': datetime.now().isoformat()
            }
    def _generate_poster_text(self, request: PosterRequest) -> Dict[str, str]:
        """
        포스터에 들어갈 텍스트 내용 생성
        Args:
            request: 포스터 생성 요청
        Returns:
            포스터 텍스트 구성 요소들
        """
        # 이미지 분석
        image_descriptions = []
        for image_path in request.image_paths:
            try:
                description = self.ai_client.analyze_image(image_path)
                image_descriptions.append(description)
            except:
                continue
        # AI 프롬프트 생성
        prompt = f"""
당신은 소상공인을 위한 포스터 카피라이터입니다.
다음 정보를 바탕으로 매력적인 포스터 문구를 작성해주세요.
**매장 정보:**
- 매장명: {request.store_name or '우리 가게'}
- 카테고리: {request.category}
- 추가 정보: {request.additional_info or '없음'}
**이벤트 정보:**
- 이벤트 제목: {request.event_title or '특별 이벤트'}
- 할인 정보: {request.discount_info or '특가 진행'}
- 시작 시간: {request.start_time or '상시'}
- 종료 시간: {request.end_time or '상시'}
**이미지 설명:**
{chr(10).join(image_descriptions) if image_descriptions else '이미지 없음'}
다음 형식으로 응답해주세요:
1. 메인 헤드라인 (10글자 이내, 임팩트 있게)
2. 서브 헤드라인 (20글자 이내, 구체적 혜택)
3. 설명 문구 (30글자 이내, 친근하고 매력적으로)
4. 행동 유도 문구 (15글자 이내, 액션 유도)
각 항목은 줄바꿈으로 구분해서 작성해주세요.
"""
        # AI로 텍스트 생성
        generated_text = self.ai_client.generate_text(prompt)
        # 생성된 텍스트 파싱
        lines = generated_text.strip().split('\n')
        return {
            'main_headline': lines[0] if len(lines) > 0 else request.event_title or '특별 이벤트',
            'sub_headline': lines[1] if len(lines) > 1 else request.discount_info or '지금 바로!',
            'description': lines[2] if len(lines) > 2 else '특별한 혜택을 놓치지 마세요',
            'call_to_action': lines[3] if len(lines) > 3 else '지금 방문하세요!'
        }
    def _process_images(self, image_paths: list) -> list:
        """
        포스터에 사용할 이미지들 전처리
        Args:
            image_paths: 원본 이미지 경로 리스트
        Returns:
            전처리된 이미지 객체 리스트
        """
        processed_images = []
        for image_path in image_paths:
            try:
                # 이미지 로드 및 리사이즈
                image = Image.open(image_path)
                # RGBA로 변환 (투명도 처리)
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')
                # 포스터에 맞게 리사이즈 (최대 400x400)
                image.thumbnail((400, 400), Image.Resampling.LANCZOS)
                processed_images.append(image)
            except Exception as e:
                print(f"이미지 처리 오류 {image_path}: {e}")
                continue
        return processed_images
    def _create_poster_image(self, request: PosterRequest, poster_text: Dict[str, str], images: list) -> Image.Image:
        """
        실제 포스터 이미지 생성
        Args:
            request: 포스터 생성 요청
            poster_text: 포스터 텍스트
            images: 전처리된 이미지 리스트
        Returns:
            생성된 포스터 이미지
        """
        # 카테고리별 테마 적용
        theme = self.category_themes.get(request.category, self.category_themes['음식'])
        # 캔버스 생성
        poster = Image.new('RGBA', 
                          (self.poster_config['width'], self.poster_config['height']), 
                          theme['background'])
        draw = ImageDraw.Draw(poster)
        # 폰트 설정 (시스템 기본 폰트 사용)
        try:
            # 다양한 폰트 시도
            title_font = ImageFont.truetype("arial.ttf", 60)
            subtitle_font = ImageFont.truetype("arial.ttf", 40)
            text_font = ImageFont.truetype("arial.ttf", 30)
            small_font = ImageFont.truetype("arial.ttf", 24)
        except:
            # 기본 폰트 사용
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        # 레이아웃 계산
        y_pos = 80
        # 1. 메인 헤드라인
        main_headline = poster_text['main_headline']
        bbox = draw.textbbox((0, 0), main_headline, font=title_font)
        text_width = bbox[2] - bbox[0]
        x_pos = (self.poster_config['width'] - text_width) // 2
        draw.text((x_pos, y_pos), main_headline, 
                 fill=theme['primary'], font=title_font)
        y_pos += 100
        # 2. 서브 헤드라인
        sub_headline = poster_text['sub_headline']
        bbox = draw.textbbox((0, 0), sub_headline, font=subtitle_font)
        text_width = bbox[2] - bbox[0]
        x_pos = (self.poster_config['width'] - text_width) // 2
        draw.text((x_pos, y_pos), sub_headline, 
                 fill=theme['secondary'], font=subtitle_font)
        y_pos += 80
        # 3. 이미지 배치 (있는 경우)
        if images:
            image_y = y_pos + 30
            if len(images) == 1:
                # 단일 이미지: 중앙 배치
                img = images[0]
                img_x = (self.poster_config['width'] - img.width) // 2
                poster.paste(img, (img_x, image_y), img)
                y_pos = image_y + img.height + 50
            elif len(images) == 2:
                # 두 개 이미지: 나란히 배치
                total_width = sum(img.width for img in images) + 20
                start_x = (self.poster_config['width'] - total_width) // 2
                for i, img in enumerate(images):
                    img_x = start_x + (i * (img.width + 20))
                    poster.paste(img, (img_x, image_y), img)
                y_pos = image_y + max(img.height for img in images) + 50
            else:
                # 여러 이미지: 그리드 형태
                cols = 2
                rows = (len(images) + cols - 1) // cols
                img_spacing = 20
                for i, img in enumerate(images[:4]):  # 최대 4개
                    row = i // cols
                    col = i % cols
                    img_x = (self.poster_config['width'] // cols) * col + \
                           (self.poster_config['width'] // cols - img.width) // 2
                    img_y = image_y + row * (200 + img_spacing)
                    poster.paste(img, (img_x, img_y), img)
                y_pos = image_y + rows * (200 + img_spacing) + 30
        # 4. 설명 문구
        description = poster_text['description']
        # 긴 텍스트는 줄바꿈 처리
        words = description.split()
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=text_font)
            if bbox[2] - bbox[0] < self.poster_config['width'] - 100:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=text_font)
            text_width = bbox[2] - bbox[0]
            x_pos = (self.poster_config['width'] - text_width) // 2
            draw.text((x_pos, y_pos), line, fill=(80, 80, 80), font=text_font)
            y_pos += 40
        y_pos += 30
        # 5. 기간 정보 (있는 경우)
        if request.start_time and request.end_time:
            period_text = f"기간: {request.start_time} ~ {request.end_time}"
            bbox = draw.textbbox((0, 0), period_text, font=small_font)
            text_width = bbox[2] - bbox[0]
            x_pos = (self.poster_config['width'] - text_width) // 2
            draw.text((x_pos, y_pos), period_text, fill=(120, 120, 120), font=small_font)
            y_pos += 50
        # 6. 행동 유도 문구 (버튼 스타일)
        cta_text = poster_text['call_to_action']
        bbox = draw.textbbox((0, 0), cta_text, font=subtitle_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        # 버튼 배경
        button_width = text_width + 60
        button_height = text_height + 30
        button_x = (self.poster_config['width'] - button_width) // 2
        button_y = self.poster_config['height'] - 150
        draw.rounded_rectangle([button_x, button_y, button_x + button_width, button_y + button_height],
                              radius=25, fill=theme['primary'])
        # 버튼 텍스트
        text_x = button_x + (button_width - text_width) // 2
        text_y = button_y + (button_height - text_height) // 2
        draw.text((text_x, text_y), cta_text, fill=(255, 255, 255), font=subtitle_font)
        # 7. 매장명 (하단)
        if request.store_name:
            store_text = request.store_name
            bbox = draw.textbbox((0, 0), store_text, font=text_font)
            text_width = bbox[2] - bbox[0]
            x_pos = (self.poster_config['width'] - text_width) // 2
            y_pos = self.poster_config['height'] - 50
            draw.text((x_pos, y_pos), store_text, fill=(100, 100, 100), font=text_font)
        return poster
    def _encode_image_to_base64(self, image: Image.Image) -> str:
        """
        PIL 이미지를 base64 문자열로 인코딩
        Args:
            image: PIL 이미지 객체
        Returns:
            base64 인코딩된 이미지 문자열
        """
        import io
        # RGB로 변환 (JPEG 저장을 위해)
        if image.mode == 'RGBA':
            # 흰색 배경과 합성
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            image = background
        # 바이트 스트림으로 변환
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='JPEG', quality=90)
        img_buffer.seek(0)
        # base64 인코딩
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        return f"data:image/jpeg;base64,{img_base64}"