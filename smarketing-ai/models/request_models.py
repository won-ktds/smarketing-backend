"""
요청 모델 정의
API 요청 데이터 구조를 정의
"""
from dataclasses import dataclass
from typing import List, Optional
@dataclass
class ContentRequest:
    """마케팅 콘텐츠 생성 요청 모델"""
    category: str  # 음식, 매장, 이벤트
    platform: str  # 네이버 블로그, 인스타그램
    image_paths: List[str]  # 업로드된 이미지 파일 경로들
    start_time: Optional[str] = None  # 이벤트 시작 시간
    end_time: Optional[str] = None    # 이벤트 종료 시간
    store_name: Optional[str] = None  # 매장명
    additional_info: Optional[str] = None  # 추가 정보
@dataclass
class PosterRequest:
    """홍보 포스터 생성 요청 모델"""
    category: str  # 음식, 매장, 이벤트
    image_paths: List[str]  # 업로드된 이미지 파일 경로들
    start_time: Optional[str] = None  # 이벤트 시작 시간
    end_time: Optional[str] = None    # 이벤트 종료 시간
    store_name: Optional[str] = None  # 매장명
    event_title: Optional[str] = None  # 이벤트 제목
    discount_info: Optional[str] = None  # 할인 정보
    additional_info: Optional[str] = None  # 추가 정보