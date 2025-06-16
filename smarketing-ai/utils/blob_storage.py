"""
Azure Blob Storage 유틸리티
이미지 업로드 및 URL 생성 기능 제공
"""
import os
from datetime import datetime
from typing import Optional
from azure.storage.blob import BlobServiceClient, ContentSettings
from config.config import Config


class BlobStorageClient:
    """Azure Blob Storage 클라이언트 클래스"""

    def __init__(self):
        """Blob Storage 클라이언트 초기화"""
        self.account_name = Config.AZURE_STORAGE_ACCOUNT_NAME
        self.account_key = Config.AZURE_STORAGE_ACCOUNT_KEY
        self.container_name = Config.AZURE_STORAGE_CONTAINER_NAME

        if not self.account_key:
            raise ValueError("Azure Storage Account Key가 설정되지 않았습니다.")

        # Connection String 생성
        connection_string = f"DefaultEndpointsProtocol=https;AccountName={self.account_name};AccountKey={self.account_key};EndpointSuffix=core.windows.net"

        # Blob Service Client 초기화
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    def upload_image(self, image_data: bytes, file_extension: str = 'png') -> str:
        """
        이미지를 Blob Storage에 업로드

        Args:
            image_data: 업로드할 이미지 바이트 데이터
            file_extension: 파일 확장자 (기본값: 'png')

        Returns:
            업로드된 이미지의 Public URL
        """
        try:
            # 파일명 생성: poster_YYYYMMDDHHMMSS.png
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            blob_name = f"poster_{timestamp}.{file_extension}"

            # Content Type 설정
            content_settings = ContentSettings(content_type=f'image/{file_extension}')

            # Blob 업로드
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )

            blob_client.upload_blob(
                image_data,
                content_settings=content_settings,
                overwrite=True
            )

            # Public URL 생성
            blob_url = f"https://{self.account_name}.blob.core.windows.net/{self.container_name}/{blob_name}"

            print(f"✅ 이미지 업로드 완료: {blob_url}")
            return blob_url

        except Exception as e:
            print(f"❌ Blob Storage 업로드 실패: {str(e)}")
            raise Exception(f"이미지 업로드 실패: {str(e)}")

    def upload_file(self, file_path: str) -> str:
        """
        로컬 파일을 Blob Storage에 업로드

        Args:
            file_path: 업로드할 로컬 파일 경로

        Returns:
            업로드된 파일의 Public URL
        """
        try:
            # 파일 확장자 추출
            file_extension = os.path.splitext(file_path)[1][1:].lower()

            # 파일 읽기
            with open(file_path, 'rb') as file:
                file_data = file.read()

            # 업로드
            return self.upload_image(file_data, file_extension)

        except Exception as e:
            print(f"❌ 파일 업로드 실패: {str(e)}")
            raise Exception(f"파일 업로드 실패: {str(e)}")

    def delete_blob(self, blob_name: str) -> bool:
        """
        Blob 삭제

        Args:
            blob_name: 삭제할 Blob 이름

        Returns:
            삭제 성공 여부
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            blob_client.delete_blob()
            print(f"✅ Blob 삭제 완료: {blob_name}")
            return True

        except Exception as e:
            print(f"❌ Blob 삭제 실패: {str(e)}")
            return False