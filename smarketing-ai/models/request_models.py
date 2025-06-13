"""
요청 모델 정의
API 요청 데이터 구조를 정의
"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import date


@dataclass
class SnsContentGetRequest:
    """SNS 게시물 생성 요청 모델"""
    title: str
    category: str
    contentType: str
    platform: str
    images: List[str]  # 이미지 URL 리스트
    requirement: Optional[str] = None
    toneAndManner: Optional[str] = None
    emotionIntensity: Optional[str] = None
    menuName: Optional[str] = None
    eventName: Optional[str] = None
    startDate: Optional[date] = None  # LocalDate -> date
    endDate: Optional[date] = None  # LocalDate -> date


@dataclass
class PosterContentGetRequest:
    """홍보 포스터 생성 요청 모델"""
    title: str
    category: str
    contentType: str
    images: List[str]  # 이미지 URL 리스트
    photoStyle: Optional[str] = None
    requirement: Optional[str] = None
    toneAndManner: Optional[str] = None
    emotionIntensity: Optional[str] = None
    menuName: Optional[str] = None
    eventName: Optional[str] = None
    startDate: Optional[date] = None  # LocalDate -> date
    endDate: Optional[date] = None  # LocalDate -> date


# 기존 모델들은 유지
@dataclass
class ContentRequest:
    """마케팅 콘텐츠 생성 요청 모델 (기존)"""
    category: str
    platform: str
    image_paths: List[str]
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    store_name: Optional[str] = None
    additional_info: Optional[str] = None


@dataclass
class PosterRequest:
    """홍보 포스터 생성 요청 모델 (기존)"""
    category: str
    image_paths: List[str]
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    store_name: Optional[str] = None
    event_title: Optional[str] = None
    discount_info: Optional[str] = None
    additional_info: Optional[str] = None
