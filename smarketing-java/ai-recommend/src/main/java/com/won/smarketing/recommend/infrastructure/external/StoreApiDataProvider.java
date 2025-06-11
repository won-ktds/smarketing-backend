package com.won.smarketing.recommend.infrastructure.external;

import com.won.smarketing.common.exception.BusinessException;
import com.won.smarketing.common.exception.ErrorCode;
import com.won.smarketing.recommend.domain.model.StoreData;
import com.won.smarketing.recommend.domain.service.StoreDataProvider;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;

import java.time.Duration;

/**
 * 매장 API 데이터 제공자 구현체
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class StoreApiDataProvider implements StoreDataProvider {

    private final WebClient webClient;

    @Value("${external.store-service.base-url}")
    private String storeServiceBaseUrl;

    @Value("${external.store-service.timeout}")
    private int timeout;

    @Override
    @Cacheable(value = "storeData", key = "#storeId")
    public StoreData getStoreData(Long storeId) {
        try {
            log.debug("매장 정보 조회 시도: storeId={}", storeId);

            // 외부 서비스 연결 시도, 실패 시 Mock 데이터 반환
            if (isStoreServiceAvailable()) {
                return callStoreService(storeId);
            } else {
                log.warn("매장 서비스 연결 불가, Mock 데이터 반환: storeId={}", storeId);
                return createMockStoreData(storeId);
            }

        } catch (Exception e) {
            log.error("매장 정보 조회 실패, Mock 데이터 반환: storeId={}", storeId, e);
            return createMockStoreData(storeId);
        }
    }

    private boolean isStoreServiceAvailable() {
        return !storeServiceBaseUrl.equals("http://localhost:8082");
    }

    private StoreData callStoreService(Long storeId) {
        try {
            StoreApiResponse response = webClient
                    .get()
                    .uri(storeServiceBaseUrl + "/api/store/" + storeId)
                    .retrieve()
                    .bodyToMono(StoreApiResponse.class)
                    .timeout(Duration.ofMillis(timeout))
                    .block();

            if (response != null && response.getData() != null) {
                StoreApiResponse.StoreInfo storeInfo = response.getData();
                return StoreData.builder()
                        .storeName(storeInfo.getStoreName())
                        .businessType(storeInfo.getBusinessType())
                        .location(storeInfo.getAddress())
                        .build();
            }
        } catch (WebClientResponseException e) {
            if (e.getStatusCode().value() == 404) {
                throw new BusinessException(ErrorCode.STORE_NOT_FOUND);
            }
            log.error("매장 서비스 호출 실패: {}", e.getMessage());
        }

        return createMockStoreData(storeId);
    }

    private StoreData createMockStoreData(Long storeId) {
        return StoreData.builder()
                .storeName("테스트 카페 " + storeId)
                .businessType("카페")
                .location("서울시 강남구")
                .build();
    }

    private static class StoreApiResponse {
        private int status;
        private String message;
        private StoreInfo data;

        public int getStatus() { return status; }
        public void setStatus(int status) { this.status = status; }
        public String getMessage() { return message; }
        public void setMessage(String message) { this.message = message; }
        public StoreInfo getData() { return data; }
        public void setData(StoreInfo data) { this.data = data; }

        static class StoreInfo {
            private Long storeId;
            private String storeName;
            private String businessType;
            private String address;
            private String phoneNumber;

            public Long getStoreId() { return storeId; }
            public void setStoreId(Long storeId) { this.storeId = storeId; }
            public String getStoreName() { return storeName; }
            public void setStoreName(String storeName) { this.storeName = storeName; }
            public String getBusinessType() { return businessType; }
            public void setBusinessType(String businessType) { this.businessType = businessType; }
            public String getAddress() { return address; }
            public void setAddress(String address) { this.address = address; }
            public String getPhoneNumber() { return phoneNumber; }
            public void setPhoneNumber(String phoneNumber) { this.phoneNumber = phoneNumber; }
        }
    }
}