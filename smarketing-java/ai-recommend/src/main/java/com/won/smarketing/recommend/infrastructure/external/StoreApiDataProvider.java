package com.won.smarketing.recommend.infrastructure.external;

import com.won.smarketing.common.exception.BusinessException;
import com.won.smarketing.common.exception.ErrorCode;
import com.won.smarketing.recommend.domain.model.StoreData;
import com.won.smarketing.recommend.domain.service.StoreDataProvider;
import jakarta.servlet.http.HttpServletRequest;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;

import java.time.Duration;

/**
 * 매장 API 데이터 제공자 구현체
 */
@Slf4j
@Service  // 추가된 어노테이션
@RequiredArgsConstructor
public class StoreApiDataProvider implements StoreDataProvider {

    private final WebClient webClient;

    @Value("${external.store-service.base-url}")
    private String storeServiceBaseUrl;

    @Value("${external.store-service.timeout}")
    private int timeout;

    private static final String AUTHORIZATION_HEADER = "Authorization";
    private static final String BEARER_PREFIX = "Bearer ";

    /**
     * 사용자 ID로 매장 정보 조회
     *
     * @param userId 사용자 ID
     * @return 매장 정보
     */
    @Override
    public StoreData getStoreDataByUserId(String userId) {
        try {
            log.debug("매장 정보 실시간 조회: userId={}", userId);
            return callStoreServiceByUserId(userId);

        } catch (Exception e) {
            log.error("매장 정보 조회 실패, Mock 데이터 반환: userId={}, error={}", userId, e.getMessage());
            return createMockStoreData(userId);
        }
    }

    private StoreData callStoreServiceByUserId(String userId) {

        try {
            StoreApiResponse response = webClient
                    .get()
                    .uri(storeServiceBaseUrl + "/api/store")
                    .header("Authorization", "Bearer " + getCurrentJwtToken())  // JWT 토큰 추가
                    .retrieve()
                    .bodyToMono(StoreApiResponse.class)
                    .timeout(Duration.ofMillis(timeout))
                    .block();

            log.info("response : {}", response.getData().getStoreName());
            log.info("response : {}", response.getData().getStoreId());

            if (response != null && response.getData() != null) {
                StoreApiResponse.StoreInfo storeInfo = response.getData();
                return StoreData.builder()
                        .storeId(storeInfo.getStoreId())
                        .storeName(storeInfo.getStoreName())
                        .businessType(storeInfo.getBusinessType())
                        .location(storeInfo.getAddress())
                        .description(storeInfo.getDescription())
                        .seatCount(storeInfo.getSeatCount())
                        .build();
            }
        } catch (WebClientResponseException e) {
            if (e.getStatusCode().value() == 404) {
                throw new BusinessException(ErrorCode.STORE_NOT_FOUND);
            }
            log.error("매장 서비스 호출 실패: {}", e.getMessage());
        }

        return createMockStoreData(userId);
    }

    private String getCurrentUserId() {
        try {
            return SecurityContextHolder.getContext().getAuthentication().getName();
        } catch (Exception e) {
            log.warn("사용자 ID 조회 실패: {}", e.getMessage());
            return null;
        }
    }

    private String getCurrentJwtToken() {
        try {
            ServletRequestAttributes attributes = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();

            if (attributes == null) {
                log.warn("RequestAttributes를 찾을 수 없음 - HTTP 요청 컨텍스트 없음");
                return null;
            }

            HttpServletRequest request = attributes.getRequest();
            String bearerToken = request.getHeader(AUTHORIZATION_HEADER);

            if (StringUtils.hasText(bearerToken) && bearerToken.startsWith(BEARER_PREFIX)) {
                String token = bearerToken.substring(BEARER_PREFIX.length());
                log.debug("JWT 토큰 추출 성공: {}...", token.substring(0, Math.min(10, token.length())));
                return token;
            } else {
                log.warn("Authorization 헤더에서 Bearer 토큰을 찾을 수 없음: {}", bearerToken);
                return null;
            }

        } catch (Exception e) {
            log.error("JWT 토큰 추출 중 오류 발생: {}", e.getMessage());
            return null;
        }
    }

    private StoreData createMockStoreData(String userId) {
        return StoreData.builder()
                .storeName("테스트 카페 " + userId)
                .businessType("카페")
                .location("서울시 강남구")
                .build();
    }

    @Getter
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

        @Getter
        static class StoreInfo {
            private Long storeId;
            private String storeName;
            private String businessType;
            private String address;
            private String description;
            private Integer seatCount;
        }
    }
}