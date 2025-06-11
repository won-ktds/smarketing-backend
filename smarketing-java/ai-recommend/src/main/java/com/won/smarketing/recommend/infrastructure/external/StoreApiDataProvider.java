package com.won.smarketing.recommend.infrastructure.external;

import com.won.smarketing.common.exception.BusinessException;
import com.won.smarketing.common.exception.ErrorCode;
import com.won.smarketing.recommend.domain.model.StoreData;
import com.won.smarketing.recommend.domain.service.StoreDataProvider;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import reactor.core.publisher.Mono;

import java.time.Duration;

/**
 * 매장 API 데이터 제공자 구현체
 * 외부 매장 서비스 API를 통해 매장 정보 조회
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class StoreApiDataProvider implements StoreDataProvider {

    private final WebClient webClient;

    @Value("${external.store-service.base-url}")
    private String storeServiceBaseUrl;

    /**
     * 매장 ID로 매장 데이터 조회
     * 
     * @param storeId 매장 ID
     * @return 매장 데이터
     */
    @Override
    public StoreData getStoreData(Long storeId) {
        try {
            log.debug("매장 정보 조회 시작: storeId={}", storeId);
            
            StoreApiResponse response = webClient
                    .get()
                    .uri(storeServiceBaseUrl + "/api/store?storeId=" + storeId)
                    .retrieve()
                    .bodyToMono(StoreApiResponse.class)
                    .timeout(Duration.ofSeconds(10))
                    .block();

            if (response == null || response.getData() == null) {
                throw new BusinessException(ErrorCode.STORE_NOT_FOUND);
            }

            StoreApiData storeApiData = response.getData();
            
            StoreData storeData = StoreData.builder()
                    .storeName(storeApiData.getStoreName())
                    .businessType(storeApiData.getBusinessType())
                    .location(storeApiData.getAddress())
                    .build();

            log.debug("매장 정보 조회 완료: {}", storeData.getStoreName());
            return storeData;

        } catch (WebClientResponseException e) {
            log.error("매장 서비스 API 호출 실패: storeId={}, status={}", storeId, e.getStatusCode(), e);
            throw new BusinessException(ErrorCode.EXTERNAL_API_ERROR);
        } catch (Exception e) {
            log.error("매장 정보 조회 중 오류 발생: storeId={}", storeId, e);
            throw new BusinessException(ErrorCode.EXTERNAL_API_ERROR);
        }
    }

    /**
     * 매장 API 응답 DTO
     */
    private static class StoreApiResponse {
        private int status;
        private String message;
        private StoreApiData data;

        // Getters and Setters
        public int getStatus() { return status; }
        public void setStatus(int status) { this.status = status; }
        public String getMessage() { return message; }
        public void setMessage(String message) { this.message = message; }
        public StoreApiData getData() { return data; }
        public void setData(StoreApiData data) { this.data = data; }
    }

    /**
     * 매장 API 데이터 DTO
     */
    private static class StoreApiData {
        private Long storeId;
        private String storeName;
        private String businessType;
        private String address;

        // Getters and Setters
        public Long getStoreId() { return storeId; }
        public void setStoreId(Long storeId) { this.storeId = storeId; }
        public String getStoreName() { return storeName; }
        public void setStoreName(String storeName) { this.storeName = storeName; }
        public String getBusinessType() { return businessType; }
        public void setBusinessType(String businessType) { this.businessType = businessType; }
        public String getAddress() { return address; }
        public void setAddress(String address) { this.address = address; }
    }
}
