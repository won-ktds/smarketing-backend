"""
마케팅 팁 생성 서비스
Java 서비스에서 요청받은 매장 정보를 기반으로 AI 마케팅 팁을 생성
"""
import os
import logging
from typing import Dict, Any, Optional
import anthropic
import openai
from datetime import datetime

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MarketingTipService:
    """마케팅 팁 생성 서비스 클래스"""
    
    def __init__(self):
        """서비스 초기화"""
        self.claude_api_key = os.getenv('CLAUDE_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        # Claude 클라이언트 초기화
        if self.claude_api_key:
            self.claude_client = anthropic.Anthropic(api_key=self.claude_api_key)
        else:
            self.claude_client = None
            logger.warning("Claude API 키가 설정되지 않았습니다.")
        
        # OpenAI 클라이언트 초기화
        if self.openai_api_key:
            self.openai_client = openai.OpenAI(api_key=self.openai_api_key)
        else:
            self.openai_client = None
            logger.warning("OpenAI API 키가 설정되지 않았습니다.")
    
    def generate_marketing_tip(self, store_data: Dict[str, Any], additional_requirement: Optional[str] = None) -> Dict[str, Any]:
        """
        매장 정보를 기반으로 AI 마케팅 팁 생성
        
        Args:
            store_data: 매장 정보 (store_name, business_type, location 등)
            
        Returns:
            생성된 마케팅 팁과 메타데이터
        """
        try:
            logger.info(f"마케팅 팁 생성 시작: {store_data.get('store_name', 'Unknown')}")
            
            # 1. 프롬프트 생성
            prompt = self._create_marketing_prompt(store_data, additional_requirement)
            
            # 2. AI 서비스 호출 (Claude 우선, 실패 시 OpenAI)
            tip_content = self._call_ai_service(prompt)
            
            # 3. 응답 데이터 구성
            response = {
                'tip': tip_content,
                'status': 'success',
                'message': 'AI 마케팅 팁이 성공적으로 생성되었습니다.',
                'generated_at': datetime.now().isoformat(),
                'store_name': store_data.get('store_name', ''),
                'business_type': store_data.get('business_type', ''),
                'ai_model': 'claude' if self.claude_client else 'openai'
            }
            
            logger.info(f"마케팅 팁 생성 완료: {store_data.get('store_name', 'Unknown')}")
            logger.info(f"마케팅 팁 생성 완료: {response}")
            return response
            
        except Exception as e:
            logger.error(f"마케팅 팁 생성 실패: {str(e)}")
            
            # 실패 시 Fallback 팁 반환
            fallback_tip = self._create_fallback_tip(store_data, additional_requirement)
            
            return {
                'tip': fallback_tip,
                'status': 'fallback',
                'message': 'AI 서비스 호출 실패로 기본 팁을 제공합니다.',
                'generated_at': datetime.now().isoformat(),
                'store_name': store_data.get('store_name', ''),
                'business_type': store_data.get('business_type', ''),
                'ai_model': 'fallback'
            }
    
    def _create_marketing_prompt(self, store_data: Dict[str, Any], additional_requirement: Optional[str]) -> str:
        """마케팅 팁 생성을 위한 프롬프트 생성"""
        
        store_name = store_data.get('store_name', '매장')
        business_type = store_data.get('business_type', '소상공인')
        location = store_data.get('location', '')
        seat_count = store_data.get('seat_count', 0)
        menu_list = store_data.get('menu_list', [])
        
        prompt = f"""
당신은 소상공인 마케팅 전문가입니다.
현재 유행하고 성공한 마케팅 예시를 검색하여 확인 한 후, 참고하여 아래 내용을 작성해주세요.

당신의 임무는 매장 정보를 바탕으로, 적은 비용으로 효과를 낼 수 있는 현실적이고 실행 가능한 마케팅 팁을 제안하는 것입니다.
지역성, 지역의 현재 날씨 확인하고, 현재 트렌드까지 고려해주세요.
소상공인을 위한 현실적이고 바로 실행할 수 있는 실용적인 마케팅 팁을 생성해주세요.
협업보다는 할인, 포스팅 등 당장 실현 가능한 현실적이면서도 창의적인 방법을 추천해주세요.

매장 정보:
- 매장명: {store_name}
- 업종: {business_type}
- 위치: {location}
- 좌석 수: {seat_count}석

"""
        # 🔥 메뉴 정보 추가
        if menu_list and len(menu_list) > 0:
            prompt += f"\n메뉴 정보:\n"
            for menu in menu_list:
                menu_name = menu.get('menu_name', '')
                category = menu.get('category', '')
                price = menu.get('price', 0)
                description = menu.get('description', '')
                prompt += f"- {menu_name} ({category}): {price:,}원 - {description}\n"
        
        prompt += """
아래 조건을 모두 충족하는 마케팅 팁을 하나 생성해주세요:

1. **실행 가능성**: 소상공인이 실제로 바로 적용할 수 있는 현실적인 방법
2. **비용 효율성**: 적은 비용으로 높은 효과를 기대할 수 있는 전략
3. **구체성**: 실행 단계가 명확하고 구체적일 것
4. **시의성**: 현재 계절, 유행, 트렌드를 반영
5. **지역성**: 지역 특성 및 현재 날씨를 고려할 것

출력해야할 내용:
- 핵심 마케팅 팁 (1개)
- 실행 방법 (1개)
- 예상 비용과 기대 효과
- 주의사항 또는 유의점
- 참고했던 실제 성공한 마케팅
- 오늘의 응원의 문장 (간결하게 1개)

아래 HTML 템플릿 형식으로 응답해주세요. <h3> 태그는 절대 변경하지 말고, <p> 태그 내용만 새로 작성해주세요
<p> 태그 내용 외에 다른 내용은 절대 넣지 마세요 :

<h3>✨ 핵심 마케팅 팁</h3>
<p>[여기에 새로운 핵심 마케팅 팁 작성]</p>

<h3>🚀 실행 방법</h3>
<p>[여기에 새로운 실행 방법 내용 작성]</p>

<h3>💰 예상 비용과 기대 효과</h3>
<p>[여기에 새로운 비용/효과 내용 작성]</p>

<h3>⚠️ 주의사항</h3>
<p>[여기에 새로운 주의사항 내용 작성]</p>

<h3>📈 참고했던 실제 성공한 마케팅</h3>
<p>[여기에 새로운 참고 사례 내용 작성, 존재하지 않는 사례는 절대 참고하지 말고, 실제 존재하는 마케팅 성공 사례로만 작성. 참고했던 존재하는 url로 함께 표기]</p>

<h3>🙌 오늘의 응원의 문장</h3>
<p>[여기에 응원의 문장 작성]</p>

심호흡하고, 단계별로 차근차근 생각해서 정확하고 실현 가능한 아이디어를 제시해주세요.
"""
        
        return prompt
    
    def _call_ai_service(self, prompt: str) -> str:
        """AI 서비스 호출"""
        
        # Claude API 우선 시도
        if self.claude_client:
            try:
                response = self.claude_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1000,
                    temperature=0.7,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                
                if response.content and len(response.content) > 0:
                    logger.info(f"마케팅 팁 생성 완료: {response.content}")
                    return response.content[0].text.strip()
                
            except Exception as e:
                logger.warning(f"Claude API 호출 실패: {str(e)}")
        
        # OpenAI API 시도
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "당신은 소상공인을 위한 마케팅 전문가입니다. 실용적이고 구체적인 마케팅 조언을 제공해주세요."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=800,
                    temperature=0.7
                )
                
                if response.choices and len(response.choices) > 0:
                    return response.choices[0].message.content.strip()
                    
            except Exception as e:
                logger.warning(f"OpenAI API 호출 실패: {str(e)}")
        
        # 모든 AI 서비스 호출 실패
        raise Exception("모든 AI 서비스 호출에 실패했습니다.")
    
    def _create_fallback_tip(self, store_data: Dict[str, Any], additional_requirement: Optional[str]) -> str:
        """AI 서비스 실패 시 규칙 기반 Fallback 팁 생성"""
        
        store_name = store_data.get('store_name', '매장')
        business_type = store_data.get('business_type', '')
        location = store_data.get('location', '')
        menu_list = store_data.get('menu_list', [])

        if menu_list and len(menu_list) > 0:
            # 가장 비싼 메뉴 찾기 (시그니처 메뉴로 가정)
            expensive_menu = max(menu_list, key=lambda x: x.get('price', 0), default=None)
            
            # 카테고리별 메뉴 분석
            categories = {}
            for menu in menu_list:
                category = menu.get('category', '기타')
                if category not in categories:
                    categories[category] = []
                categories[category].append(menu)
            
            main_category = max(categories.keys(), key=lambda x: len(categories[x])) if categories else '메뉴'
            
            if expensive_menu:
                signature_menu = expensive_menu.get('menu_name', '시그니처 메뉴')
                return f"""🎯 {store_name} 메뉴 기반 마케팅 전략

💡 핵심 전략:
- SNS를 활용한 홍보 강화
- 고객 리뷰 관리 및 적극 활용
- 지역 커뮤니티 참여로 인지도 향상

📱 실행 방법:
1. 인스타그램/네이버 블로그 정기 포스팅
2. 고객 만족도 조사 및 피드백 반영
3. 주변 상권과의 협력 이벤트 기획

💰 예상 효과: 월 매출 10-15% 증가 가능
⚠️ 주의사항: 꾸준한 실행과 고객 소통이 핵심"""
        
        # 업종별 기본 팁
        if '카페' in business_type or '커피' in business_type:
            return f"""☕ {store_name} 카페 마케팅 전략

💡 핵심 포인트:
1. 시그니처 음료 개발 및 SNS 홍보
2. 계절별 한정 메뉴로 재방문 유도
3. 인스타그램 포토존 설치

📱 실행 방법:
- 매주 신메뉴 또는 이벤트 인스타 포스팅
- 고객 사진 리포스트로 참여 유도
- 해시태그 #근처카페 #데이트코스 활용

💰 비용: 월 5-10만원 내외
📈 기대효과: 젊은 고객층 20% 증가"""
            
        elif '음식점' in business_type or '식당' in business_type:
            return f"""🍽️ {store_name} 음식점 마케팅 전략

💡 핵심 포인트:
1. 대표 메뉴 스토리텔링
2. 배달앱 리뷰 관리 강화
3. 단골 고객 혜택 프로그램

📱 실행 방법:
- 요리 과정 영상으로 신뢰도 구축
- 리뷰 적극 답변으로 고객 관리
- 방문 횟수별 할인 혜택 제공

💰 비용: 월 3-7만원 내외
📈 기대효과: 재방문율 25% 향상"""
            
        elif '베이커리' in business_type or '빵집' in business_type:
            return f"""🍞 {store_name} 베이커리 마케팅 전략

💡 핵심 포인트:
1. 갓 구운 빵 타이밍 알림 서비스
2. 계절 한정 빵 출시
3. 포장 디자인으로 선물용 어필

📱 실행 방법:
- 네이버 톡톡으로 빵 완성 시간 안내
- 명절/기념일 특별 빵 한정 판매
- 예쁜 포장지로 브랜딩 강화

💰 비용: 월 5-8만원 내외
📈 기대효과: 단골 고객 30% 증가"""
        
        # 지역별 특성 고려
        if location:
            location_tip = ""
            if '강남' in location or '서초' in location:
                location_tip = "\n🏢 강남권 특화: 직장인 대상 점심 세트메뉴 강화"
            elif '홍대' in location or '신촌' in location:
                location_tip = "\n🎓 대학가 특화: 학생 할인 및 그룹 이벤트 진행"
            elif '강북' in location or '노원' in location:
                location_tip = "\n🏘️ 주거지역 특화: 가족 단위 고객 대상 패키지 상품"
            
            return f"""🎯 {store_name} 지역 맞춤 마케팅

💡 기본 전략:
- 온라인 리뷰 관리 강화
- 단골 고객 혜택 프로그램
- 지역 커뮤니티 참여{location_tip}

📱 실행 방법:
1. 구글/네이버 지도 정보 최신화
2. 동네 맘카페 홍보 참여
3. 주변 상권과 상생 이벤트

💰 비용: 월 3-5만원
📈 기대효과: 인지도 및 매출 향상"""
        
        # 기본 범용 팁
        return f"""🎯 {store_name} 기본 마케팅 전략

💡 핵심 3가지:
1. 온라인 존재감 강화 (SNS, 리뷰 관리)
2. 고객 소통 및 피드백 활용
3. 차별화된 서비스 제공

📱 실행 방법:
- 네이버 플레이스, 구글 정보 최신화
- 고객 불만 신속 해결로 신뢰 구축
- 작은 이벤트라도 꾸준히 진행

💰 비용: 거의 무료 (시간 투자 위주)
📈 기대효과: 꾸준한 성장과 단골 확보

⚠️ 핵심은 지속성입니다!"""
