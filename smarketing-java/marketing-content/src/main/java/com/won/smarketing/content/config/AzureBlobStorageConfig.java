// store/src/main/java/com/won/smarketing/store/config/AzureBlobStorageConfig.java
package com.won.smarketing.content.config;

import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.storage.blob.BlobServiceClient;
import com.azure.storage.blob.BlobServiceClientBuilder;
import com.azure.storage.common.StorageSharedKeyCredential;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Azure Blob Storage 설정 클래스
 * Azure Blob Storage와의 연결을 위한 설정
 */
@Configuration
@Slf4j
public class AzureBlobStorageConfig {

    @Value("${azure.storage.account-name}")
    private String accountName;

    @Value("${azure.storage.account-key:}")
    private String accountKey;

    @Value("${azure.storage.endpoint:}")
    private String endpoint;

    /**
     * Azure Blob Storage Service Client 생성
     *
     * @return BlobServiceClient 인스턴스
     */
    @Bean
    public BlobServiceClient blobServiceClient() {
        try {
            // Managed Identity 사용 시 (Azure 환경에서 권장)
            if (accountKey == null || accountKey.isEmpty()) {
                log.info("Azure Blob Storage 연결 - Managed Identity 사용");
                return new BlobServiceClientBuilder()
                        .endpoint(getEndpoint())
                        .credential(new DefaultAzureCredentialBuilder().build())
                        .buildClient();
            }

            // Account Key 사용 시 (개발 환경용)
            log.info("Azure Blob Storage 연결 - Account Key 사용");
            StorageSharedKeyCredential credential = new StorageSharedKeyCredential(accountName, accountKey);
            return new BlobServiceClientBuilder()
                    .endpoint(getEndpoint())
                    .credential(credential)
                    .buildClient();

        } catch (Exception e) {
            log.error("Azure Blob Storage 클라이언트 생성 실패", e);
            throw new RuntimeException("Azure Blob Storage 연결 실패", e);
        }
    }

    /**
     * Storage Account 엔드포인트 URL 생성
     *
     * @return 엔드포인트 URL
     */
    private String getEndpoint() {
        if (endpoint != null && !endpoint.isEmpty()) {
            return endpoint;
        }
        return String.format("https://%s.blob.core.windows.net", accountName);
    }
}