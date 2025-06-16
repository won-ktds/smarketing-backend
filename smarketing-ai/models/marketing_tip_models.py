"""
마케팅 팁 API 요청/응답 모델
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class MenuInfo(BaseModel):
    """메뉴 정보 모델"""
    
    menu_id: int = Field(..., description="메뉴 ID")
    menu_name: str = Field(..., description="메뉴명")
    category: str = Field(..., description="메뉴 카테고리")
    price: int = Field(..., description="가격")
    description: Optional[str] = Field(None, description="메뉴 설명")
    
    class Config:
        schema_extra = {
            "example": {
                "store_name": "더블샷 카페",
                "business_type": "카페",
                "location": "서울시 강남구 역삼동",
                "seat_count": 30,
                "menu_list": [
                    {
                        "menu_id": 1,
                        "menu_name": "아메리카노",
                        "category": "음료",
                        "price": 4000,
                        "description": "깊고 진한 맛의 아메리카노"
                    },
                    {
                        "menu_id": 2,
                        "menu_name": "카페라떼",
                        "category": "음료",
                        "price": 4500,
                        "description": "부드러운 우유 거품이 올라간 카페라떼"
                    },
                    {
                        "menu_id": 3,
                        "menu_name": "치즈케이크",
                        "category": "디저트",
                        "price": 6000,
                        "description": "진한 치즈 맛의 수제 케이크"
                    }
                ],
                "additional_requirement": "젊은 고객층을 타겟으로 한 마케팅"
            }
        }

class MarketingTipGenerateRequest(BaseModel):
    """마케팅 팁 생성 요청 모델"""
    
    store_name: str = Field(..., description="매장명")
    business_type: str = Field(..., description="업종")
    location: Optional[str] = Field(None, description="위치")
    seat_count: Optional[int] = Field(None, description="좌석 수")
    menu_list: Optional[List[MenuInfo]] = Field(default=[], description="메뉴 목록")
    
    class Config:
        schema_extra = {
            "example": {
                "store_name": "더블샷 카페",
                "business_type": "카페",
                "location": "서울시 강남구 역삼동",
                "seat_count": 30,
            }
        }

class MarketingTipResponse(BaseModel):
    """마케팅 팁 응답 모델"""
    
    tip: str = Field(..., description="생성된 마케팅 팁")
    status: str = Field(..., description="응답 상태 (success, fallback, error)")
    message: str = Field(..., description="응답 메시지")
    generated_at: str = Field(..., description="생성 시간")
    store_name: str = Field(..., description="매장명")
    business_type: str = Field(..., description="업종")
    ai_model: str = Field(..., description="사용된 AI 모델")
    
    class Config:
        schema_extra = {
            "example": {
                "tip": "☕ 더블샷 카페 여름 마케팅 전략\n\n💡 핵심 포인트:\n1. 여름 한정 시원한 음료 개발\n2. SNS 이벤트로 젊은 고객층 공략\n3. 더위 피할 수 있는 쾌적한 환경 어필",
                "status": "success",
                "message": "AI 마케팅 팁이 성공적으로 생성되었습니다.",
                "generated_at": "2024-06-13T15:30:00",
                "store_name": "더블샷 카페",
                "business_type": "카페",
                "ai_model": "claude"
            }
        }
