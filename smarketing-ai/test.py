"""
마케팅 팁 API 테스트 스크립트
"""
import requests
import json


def test_marketing_tip_api():
    """마케팅 팁 API 테스트"""
    
    # 테스트 데이터
    test_data = {
        "store_name": "더블샷 카페",
        "business_type": "카페", 
        "location": "서울시 강남구 역삼동",
        "seat_count": 30,
    }
    
    # API 호출
    url = "http://localhost:5001/api/v1/generate-marketing-tip"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer dummy-key"
    }
    
    try:
        response = requests.post(url, json=test_data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 200:
            print("✅ 테스트 성공!")
        else:
            print("❌ 테스트 실패!")
            
    except Exception as e:
        print(f"❌ 테스트 오류: {str(e)}")


if __name__ == "__main__":
    test_marketing_tip_api()