"""
이미지 처리 유틸리티
이미지 분석, 변환, 최적화 기능 제공
"""
import os
from typing import Dict, Any, Tuple
from PIL import Image, ImageOps
import io
class ImageProcessor:
    """이미지 처리 클래스"""
    def __init__(self):
        """이미지 프로세서 초기화"""
        self.supported_formats = {'JPEG', 'PNG', 'WEBP', 'GIF'}
        self.max_size = (2048, 2048)  # 최대 크기
        self.thumbnail_size = (400, 400)  # 썸네일 크기
    def get_image_info(self, image_path: str) -> Dict[str, Any]:
        """
        이미지 기본 정보 추출
        Args:
            image_path: 이미지 파일 경로
        Returns:
            이미지 정보 딕셔너리
        """
        try:
            with Image.open(image_path) as image:
                info = {
                    'filename': os.path.basename(image_path),
                    'format': image.format,
                    'mode': image.mode,
                    'size': image.size,
                    'width': image.width,
                    'height': image.height,
                    'file_size': os.path.getsize(image_path),
                    'aspect_ratio': round(image.width / image.height, 2) if image.height > 0 else 0
                }
                # 이미지 특성 분석
                info['is_landscape'] = image.width > image.height
                info['is_portrait'] = image.height > image.width
                info['is_square'] = abs(image.width - image.height) < 50
                return info
        except Exception as e:
            return {
                'filename': os.path.basename(image_path),
                'error': str(e)
            }
    def resize_image(self, image_path: str, target_size: Tuple[int, int], 
                    maintain_aspect: bool = True) -> Image.Image:
        """
        이미지 크기 조정
        Args:
            image_path: 원본 이미지 경로
            target_size: 목표 크기 (width, height)
            maintain_aspect: 종횡비 유지 여부
        Returns:
            리사이즈된 PIL 이미지
        """
        try:
            with Image.open(image_path) as image:
                if maintain_aspect:
                    # 종횡비 유지하며 리사이즈
                    image.thumbnail(target_size, Image.Resampling.LANCZOS)
                    return image.copy()
                else:
                    # 강제 리사이즈
                    return image.resize(target_size, Image.Resampling.LANCZOS)
        except Exception as e:
            raise Exception(f"이미지 리사이즈 실패: {str(e)}")
    def optimize_image(self, image_path: str, quality: int = 85) -> bytes:
        """
        이미지 최적화 (파일 크기 줄이기)
        Args:
            image_path: 원본 이미지 경로
            quality: JPEG 품질 (1-100)
        Returns:
            최적화된 이미지 바이트
        """
        try:
            with Image.open(image_path) as image:
                # RGBA를 RGB로 변환 (JPEG 저장을 위해)
                if image.mode == 'RGBA':
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[-1])
                    image = background
                # 크기가 너무 크면 줄이기
                if image.width > self.max_size[0] or image.height > self.max_size[1]:
                    image.thumbnail(self.max_size, Image.Resampling.LANCZOS)
                # 바이트 스트림으로 저장
                img_buffer = io.BytesIO()
                image.save(img_buffer, format='JPEG', quality=quality, optimize=True)
                return img_buffer.getvalue()
        except Exception as e:
            raise Exception(f"이미지 최적화 실패: {str(e)}")
    def create_thumbnail(self, image_path: str, size: Tuple[int, int] = None) -> Image.Image:
        """
        썸네일 생성
        Args:
            image_path: 원본 이미지 경로
            size: 썸네일 크기 (기본값: self.thumbnail_size)
        Returns:
            썸네일 PIL 이미지
        """
        if size is None:
            size = self.thumbnail_size
        try:
            with Image.open(image_path) as image:
                # 정사각형 썸네일 생성
                thumbnail = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
                return thumbnail
        except Exception as e:
            raise Exception(f"썸네일 생성 실패: {str(e)}")
    def analyze_colors(self, image_path: str, num_colors: int = 5) -> list:
        """
        이미지의 주요 색상 추출
        Args:
            image_path: 이미지 파일 경로
            num_colors: 추출할 색상 개수
        Returns:
            주요 색상 리스트 [(R, G, B), ...]
        """
        try:
            with Image.open(image_path) as image:
                # RGB로 변환
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                # 이미지 크기 줄여서 처리 속도 향상
                image.thumbnail((150, 150))
                # 색상 히스토그램 생성
                colors = image.getcolors(maxcolors=256*256*256)
                if colors:
                    # 빈도순으로 정렬
                    colors.sort(key=lambda x: x[0], reverse=True)
                    # 상위 색상들 반환
                    dominant_colors = []
                    for count, color in colors[:num_colors]:
                        dominant_colors.append(color)
                    return dominant_colors
                return [(128, 128, 128)]  # 기본 회색
        except Exception as e:
            print(f"색상 분석 실패: {e}")
            return [(128, 128, 128)]  # 기본 회색
    def is_food_image(self, image_path: str) -> bool:
        """
        음식 이미지 여부 간단 판별
        (실제로는 AI 모델이 필요하지만, 여기서는 기본적인 휴리스틱 사용)
        Args:
            image_path: 이미지 파일 경로
        Returns:
            음식 이미지 여부
        """
        try:
            # 파일명에서 키워드 확인
            filename = os.path.basename(image_path).lower()
            food_keywords = ['food', 'meal', 'dish', 'menu', '음식', '메뉴', '요리']
            for keyword in food_keywords:
                if keyword in filename:
                    return True
            # 색상 분석으로 간단 판별 (음식은 따뜻한 색조가 많음)
            colors = self.analyze_colors(image_path, 3)
            warm_color_count = 0
            for r, g, b in colors:
                # 따뜻한 색상 (빨강, 노랑, 주황 계열) 확인
                if r > 150 or (r > g and r > b):
                    warm_color_count += 1
            return warm_color_count >= 2
        except:
            return False