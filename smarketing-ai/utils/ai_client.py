"""
AI 클라이언트 유틸리티
Claude AI 및 OpenAI API 호출을 담당
"""
import os
import base64
from typing import Optional
import anthropic
import openai
from PIL import Image
import io
class AIClient:
    """AI API 클라이언트 클래스"""
    def __init__(self):
        """AI 클라이언트 초기화"""
        self.claude_api_key = os.getenv('CLAUDE_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        # Claude 클라이언트 초기화
        if self.claude_api_key:
            self.claude_client = anthropic.Anthropic(api_key=self.claude_api_key)
        else:
            self.claude_client = None
        # OpenAI 클라이언트 초기화
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
            self.openai_client = openai
        else:
            self.openai_client = None
    def generate_text(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        텍스트 생성 (Claude 우선, 실패시 OpenAI 사용)
        Args:
            prompt: 생성할 텍스트의 프롬프트
            max_tokens: 최대 토큰 수
        Returns:
            생성된 텍스트
        """
        # Claude AI 시도
        if self.claude_client:
            try:
                response = self.claude_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=max_tokens,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.content[0].text
            except Exception as e:
                print(f"Claude AI 호출 실패: {e}")
        # OpenAI 시도
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"OpenAI 호출 실패: {e}")
        # 기본 응답 (AI 서비스 모두 실패시)
        return self._generate_fallback_content(prompt)
    def analyze_image(self, image_path: str) -> str:
        """
        이미지 분석 및 설명 생성
        Args:
            image_path: 분석할 이미지 경로
        Returns:
            이미지 설명 텍스트
        """
        try:
            # 이미지를 base64로 인코딩
            image_base64 = self._encode_image_to_base64(image_path)
            # Claude Vision API 시도
            if self.claude_client:
                try:
                    response = self.claude_client.messages.create(
                        model="claude-3-sonnet-20240229",
                        max_tokens=500,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "이 이미지를 보고 음식점 마케팅에 활용할 수 있도록 매력적으로 설명해주세요. 음식이라면 맛있어 보이는 특징을, 매장이라면 분위기를, 이벤트라면 특별함을 강조해서 한국어로 50자 이내로 설명해주세요."
                                    },
                                    {
                                        "type": "image",
                                        "source": {
                                            "type": "base64",
                                            "media_type": "image/jpeg",
                                            "data": image_base64
                                        }
                                    }
                                ]
                            }
                        ]
                    )
                    return response.content[0].text
                except Exception as e:
                    print(f"Claude 이미지 분석 실패: {e}")
            # OpenAI Vision API 시도
            if self.openai_client:
                try:
                    response = self.openai_client.chat.completions.create(
                        model="gpt-4-vision-preview",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "이 이미지를 보고 음식점 마케팅에 활용할 수 있도록 매력적으로 설명해주세요. 한국어로 50자 이내로 설명해주세요."
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{image_base64}"
                                        }
                                    }
                                ]
                            }
                        ],
                        max_tokens=300
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    print(f"OpenAI 이미지 분석 실패: {e}")
        except Exception as e:
            print(f"이미지 분석 전체 실패: {e}")
        # 기본 설명 반환
        return "맛있고 매력적인 음식점의 특별한 순간"
    def _encode_image_to_base64(self, image_path: str) -> str:
        """
        이미지 파일을 base64로 인코딩
        Args:
            image_path: 이미지 파일 경로
        Returns:
            base64 인코딩된 이미지 문자열
        """
        with open(image_path, "rb") as image_file:
            # 이미지 크기 조정 (API 제한 고려)
            image = Image.open(image_file)
            # 최대 크기 제한 (1024x1024)
            if image.width > 1024 or image.height > 1024:
                image.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
            # JPEG로 변환하여 파일 크기 줄이기
            if image.mode == 'RGBA':
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])
                image = background
            img_buffer = io.BytesIO()
            image.save(img_buffer, format='JPEG', quality=85)
            img_buffer.seek(0)
            return base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    def _generate_fallback_content(self, prompt: str) -> str:
        """
        AI 서비스 실패시 기본 콘텐츠 생성
        Args:
            prompt: 원본 프롬프트
        Returns:
            기본 콘텐츠
        """
        if "콘텐츠" in prompt or "게시글" in prompt:
            return """안녕하세요! 오늘도 맛있는 하루 되세요 😊
우리 가게의 특별한 메뉴를 소개합니다!
정성껏 준비한 음식으로 여러분을 맞이하겠습니다.
많은 관심과 사랑 부탁드려요!"""
        elif "포스터" in prompt:
            return "특별한 이벤트\n지금 바로 확인하세요\n우리 가게에서 만나요\n놓치지 마세요!"
        else:
            return "안녕하세요! 우리 가게를 찾아주셔서 감사합니다."