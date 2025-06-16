package com.won.smarketing.recommend.infrastructure.external;

import com.won.smarketing.recommend.domain.model.MenuData;
import com.won.smarketing.recommend.domain.model.StoreData;
import com.won.smarketing.recommend.domain.model.StoreWithMenuData;
import com.won.smarketing.recommend.domain.service.AiTipGenerator;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;  // 이 어노테이션이 누락되어 있었음
import org.springframework.web.reactive.function.client.WebClient;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Python AI 팁 생성 구현체 (날씨 정보 제거)
 */
@Slf4j
@Service  // 추가된 어노테이션
@RequiredArgsConstructor
public class PythonAiTipGenerator implements AiTipGenerator {

    private final WebClient webClient;

    @Value("${external.python-ai-service.base-url}")
    private String pythonAiServiceBaseUrl;

    @Value("${external.python-ai-service.api-key}")
    private String pythonAiServiceApiKey;

    @Value("${external.python-ai-service.timeout}")
    private int timeout;

    @Override
    public String generateTip(StoreWithMenuData storeWithMenuData) {
        try {
            log.debug("Python AI 서비스 직접 호출: store={}", storeWithMenuData.getStoreData().getStoreName());
            return callPythonAiService(storeWithMenuData);

        } catch (Exception e) {
            log.error("Python AI 서비스 호출 실패, Fallback 처리: {}", e.getMessage());
            return createFallbackTip(storeWithMenuData);
        }
    }

    private String callPythonAiService(StoreWithMenuData storeWithMenuData) {

        try {

            StoreData storeData = storeWithMenuData.getStoreData();
            List<MenuData> menuDataList = storeWithMenuData.getMenuDataList();

            // 메뉴 데이터를 Map 형태로 변환
            List<Map<String, Object>> menuList = menuDataList.stream()
                    .map(menu -> {
                        Map<String, Object> menuMap = new HashMap<>();
                        menuMap.put("menu_id", menu.getMenuId());
                        menuMap.put("menu_name", menu.getMenuName());
                        menuMap.put("category", menu.getCategory());
                        menuMap.put("price", menu.getPrice());
                        menuMap.put("description", menu.getDescription());
                        return menuMap;
                    })
                    .collect(Collectors.toList());

            // Python AI 서비스로 전송할 데이터 (매장 정보 + 메뉴 정보)
            Map<String, Object> requestData = new HashMap<>();
            requestData.put("store_name", storeData.getStoreName());
            requestData.put("business_type", storeData.getBusinessType());
            requestData.put("location", storeData.getLocation());
            requestData.put("seat_count", storeData.getSeatCount());
            requestData.put("menu_list", menuList);

            log.debug("Python AI 서비스 요청 데이터: {}", requestData);

            PythonAiResponse response = webClient
                    .post()
                    .uri(pythonAiServiceBaseUrl + "/api/v1/generate-marketing-tip")
                    .header("Authorization", "Bearer " + pythonAiServiceApiKey)
                    .header("Content-Type", "application/json")
                    .bodyValue(requestData)
                    .retrieve()
                    .bodyToMono(PythonAiResponse.class)
                    .timeout(Duration.ofMillis(timeout))
                    .block();

            if (response != null && response.getTip() != null && !response.getTip().trim().isEmpty()) {
                log.debug("Python AI 서비스 응답 성공: tip length={}", response.getTip().length());
                return response.getTip();
            }
        } catch (Exception e) {
            log.error("Python AI 서비스 실제 호출 실패: {}", e.getMessage());
        }

        return createFallbackTip(storeWithMenuData);
    }

    /**
     * 규칙 기반 Fallback 팁 생성 (날씨 정보 없이 매장 정보만 활용)
     */
    private String createFallbackTip(StoreWithMenuData storeWithMenuData) {
        String businessType = storeWithMenuData.getStoreData().getBusinessType();
        String storeName = storeWithMenuData.getStoreData().getStoreName();
        String location = storeWithMenuData.getStoreData().getLocation();

        // 업종별 기본 팁 생성
        if (businessType.contains("카페")) {
            return String.format("%s만의 시그니처 음료와 디저트로 고객들에게 특별한 경험을 선사해보세요!", storeName);
        } else if (businessType.contains("음식점") || businessType.contains("식당")) {
            return String.format("%s의 대표 메뉴를 활용한 특별한 이벤트로 고객들의 관심을 끌어보세요!", storeName);
        } else if (businessType.contains("베이커리") || businessType.contains("빵집")) {
            return String.format("%s의 갓 구운 빵과 함께하는 따뜻한 서비스로 고객들의 마음을 사로잡아보세요!", storeName);
        } else if (businessType.contains("치킨") || businessType.contains("튀김")) {
            return String.format("%s의 바삭하고 맛있는 메뉴로 고객들에게 만족스러운 식사를 제공해보세요!", storeName);
        }

        // 지역별 팁
        if (location.contains("강남") || location.contains("서초")) {
            return String.format("%s에서 트렌디하고 세련된 서비스로 젊은 고객층을 공략해보세요!", storeName);
        } else if (location.contains("홍대") || location.contains("신촌")) {
            return String.format("%s에서 활기차고 개성 있는 이벤트로 대학생들의 관심을 끌어보세요!", storeName);
        }

        // 기본 팁
        return String.format("%s만의 특별함을 살린 고객 맞춤 서비스로 단골 고객을 늘려보세요!", storeName);
    }

    @Getter
    private static class PythonAiResponse {
        private String tip;
        private String status;
        private String message;
        private LocalDateTime generatedTip;
        private String businessType;
        private String aiModel;
    }
}