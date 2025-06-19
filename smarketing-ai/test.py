# openai_simple_test.py
import requests
import os
from utils.ai_client import AIClient
import openai
import base64

def openai_test(prompt: str,):
    try:
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if openai_api_key:
            openai_client = openai.OpenAI(api_key=openai_api_key)
        else:
            openai_client = None

        if not openai_client:
            raise Exception("OpenAI API 키가 설정되지 않았습니다.")

        response = openai_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1,
        )


        # # Azure Blob Storage에 업로드
        # blob_url = self.blob_client.upload_image(image_data, 'png')

        print(f"✅ 이미지 생성 및 업로드 완료: {response}")
        return response

    except Exception as e:
        raise Exception(f"이미지 생성 실패: {str(e)}")

if __name__ == "__main__":
    # API 키 확인
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  환경변수 OPENAI_API_KEY가 설정되지 않았습니다.")
        print("코드 상단의 'your-api-key-here' 부분에 실제 API 키를 입력하거나")
        print("export OPENAI_API_KEY='실제키' 로 환경변수를 설정해주세요.\n")
    
    openai_test("""
""")