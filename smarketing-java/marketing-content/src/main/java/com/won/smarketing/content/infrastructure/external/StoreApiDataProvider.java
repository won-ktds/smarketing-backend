package com.won.smarketing.content.infrastructure.external;

import com.won.smarketing.common.exception.BusinessException;
import com.won.smarketing.common.exception.ErrorCode;
import com.won.smarketing.content.domain.model.store.MenuData;
import com.won.smarketing.content.domain.model.store.StoreData;
import com.won.smarketing.content.domain.model.store.StoreWithMenuData;
import com.won.smarketing.content.domain.service.StoreDataProvider;
import jakarta.servlet.http.HttpServletRequest;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientException;
import org.springframework.web.reactive.function.client.WebClientResponseException;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

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

    public StoreWithMenuData getStoreWithMenuData(String userId) {
        log.info("매장 정보와 메뉴 정보 통합 조회 시작: userId={}", userId);

        try {
            // 매장 정보와 메뉴 정보를 병렬로 조회
            StoreData storeData = getStoreDataByUserId(userId);
            List<MenuData> menuDataList = getMenusByStoreId(storeData.getStoreId());

            StoreWithMenuData result = StoreWithMenuData.builder()
                    .storeData(storeData)
                    .menuDataList(menuDataList)
                    .build();

            log.info("매장 정보와 메뉴 정보 통합 조회 완료: storeId={}, storeName={}, menuCount={}",
                    storeData.getStoreId(), storeData.getStoreName(), menuDataList.size());

            return result;

        } catch (Exception e) {
            log.error("매장 정보와 메뉴 정보 통합 조회 실패, Mock 데이터 반환: storeId={}", userId, e);

            // 실패 시 Mock 데이터 반환
            return StoreWithMenuData.builder()
                    .storeData(createMockStoreData(userId))
                    .menuDataList(createMockMenuData(6L))
                    .build();
        }
    }

    public StoreData getStoreDataByUserId(String userId) {
        try {
            log.debug("매장 정보 실시간 조회: userId={}", userId);
            return callStoreServiceByUserId(userId);

        } catch (Exception e) {
            log.error("매장 정보 조회 실패, Mock 데이터 반환: userId={}, error={}", userId, e.getMessage());
            return createMockStoreData(userId);
        }
    }


    public List<MenuData> getMenusByStoreId(Long storeId) {
        log.info("매장 메뉴 조회 시작: storeId={}", storeId);

        try {
            return callMenuService(storeId);
        } catch (Exception e) {
            log.error("메뉴 조회 실패, Mock 데이터 반환: storeId={}", storeId, e);
            return createMockMenuData(storeId);
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

    private List<MenuData> callMenuService(Long storeId) {
        try {
            MenuApiResponse response = webClient
                    .get()
                    .uri(storeServiceBaseUrl + "/api/menu/store/" + storeId)
                    .retrieve()
                    .bodyToMono(MenuApiResponse.class)
                    .timeout(Duration.ofMillis(timeout))
                    .block();

            if (response != null && response.getData() != null && !response.getData().isEmpty()) {
                List<MenuData> menuDataList = response.getData().stream()
                        .map(this::toMenuData)
                        .collect(Collectors.toList());

                log.info("매장 메뉴 조회 성공: storeId={}, menuCount={}", storeId, menuDataList.size());
                return menuDataList;
            }
        } catch (WebClientResponseException e) {
            if (e.getStatusCode().value() == 404) {
                log.warn("매장의 메뉴 정보가 없습니다: storeId={}", storeId);
                return Collections.emptyList();
            }
            log.error("메뉴 서비스 호출 실패: storeId={}, error={}", storeId, e.getMessage());
        } catch (WebClientException e) {
            log.error("메뉴 서비스 연결 실패: storeId={}, error={}", storeId, e.getMessage());
        }

        return createMockMenuData(storeId);
    }

    /**
     * MenuResponse를 MenuData로 변환
     */
    private MenuData toMenuData(MenuApiResponse.MenuInfo menuInfo) {
        return MenuData.builder()
                .menuId(menuInfo.getMenuId())
                .menuName(menuInfo.getMenuName())
                .category(menuInfo.getCategory())
                .price(menuInfo.getPrice())
                .description(menuInfo.getDescription())
                .build();
    }

    private StoreData createMockStoreData(String userId) {
        return StoreData.builder()
                .storeName("테스트 카페 " + userId)
                .businessType("카페")
                .location("서울시 강남구")
                .build();
    }

    private List<MenuData> createMockMenuData(Long storeId) {
        log.info("Mock 메뉴 데이터 생성: storeId={}", storeId);

        return List.of(
                MenuData.builder()
                        .menuId(1L)
                        .menuName("아메리카노")
                        .category("음료")
                        .price(4000)
                        .description("깊고 진한 맛의 아메리카노")
                        .build(),
                MenuData.builder()
                        .menuId(2L)
                        .menuName("카페라떼")
                        .category("음료")
                        .price(4500)
                        .description("부드러운 우유 거품이 올라간 카페라떼")
                        .build(),
                MenuData.builder()
                        .menuId(3L)
                        .menuName("치즈케이크")
                        .category("디저트")
                        .price(6000)
                        .description("진한 치즈 맛의 수제 케이크")

                        .build()
        );
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

    /**
     * Menu API 응답 DTO (새로 추가)
     */
    private static class MenuApiResponse {
        private List<MenuInfo> data;
        private String message;
        private boolean success;

        public List<MenuInfo> getData() { return data; }
        public void setData(List<MenuInfo> data) { this.data = data; }
        public String getMessage() { return message; }
        public void setMessage(String message) { this.message = message; }
        public boolean isSuccess() { return success; }
        public void setSuccess(boolean success) { this.success = success; }

        public static class MenuInfo {
            private Long menuId;
            private String menuName;
            private String category;
            private Integer price;
            private String description;
            private String image;
            private LocalDateTime createdAt;
            private LocalDateTime updatedAt;

            public Long getMenuId() { return menuId; }
            public void setMenuId(Long menuId) { this.menuId = menuId; }
            public String getMenuName() { return menuName; }
            public void setMenuName(String menuName) { this.menuName = menuName; }
            public String getCategory() { return category; }
            public void setCategory(String category) { this.category = category; }
            public Integer getPrice() { return price; }
            public void setPrice(Integer price) { this.price = price; }
            public String getDescription() { return description; }
            public void setDescription(String description) { this.description = description; }
            public String getImage() { return image; }
            public void setImage(String image) { this.image = image; }
            public LocalDateTime getCreatedAt() { return createdAt; }
            public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
            public LocalDateTime getUpdatedAt() { return updatedAt; }
            public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
        }
    }
}