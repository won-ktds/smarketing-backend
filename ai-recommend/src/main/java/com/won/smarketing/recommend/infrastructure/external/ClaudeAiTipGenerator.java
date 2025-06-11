package com.won.smarketing.recommend.infrastructure.external;

import com.won.smarketing.common.exception.BusinessException;
import com.won.smarketing.common.exception.ErrorCode;
import com.won.smarketing.recommend.domain.model.StoreData;
import com.won.smarketing.recommend.domain.model.WeatherData;
import com.won.smarketing.recommend.domain.service.AiTipGenerator;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import reactor.core.publisher.Mono;

import java.time.Duration;
import java.util.Map;

/**
 * Claude AI 팁 생성기 구현체
 * Claude AI API를 통해 마케팅 팁 생성
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class ClaudeAiTipGenerator implements AiTipGenerator {

    private final WebClient webClient;

    @Value("${external.claude-ai.api-key}")
    private String claudeApiKey;

    @Value("${external.claude-ai.base-url}")
    private String claudeApiBaseUrl;

    @Value("${external.claude-ai.model}")
    private String claudeModel;

    @Value("${external.claude-ai.max-tokens}")
    private Integer maxTokens;

    /**
     * 매장 정보와 날씨 정보를 바탕으로 마케팅 팁 생성
     * 
     * @param storeData 매장 데이터
     * @param weatherData 날씨 데이터
     * @return AI가 생성한 마케팅 팁
     */
    @Override
    public String generateTip(StoreData storeData, WeatherData weatherData) {
        try {
            log.debug("AI 마케팅 팁 생성 시작: store={}, weather={}도", 
                     storeData.getStoreName(), weatherData.getTemperature());

            String prompt = buildPrompt(storeData, weatherData);
            
            Map<String, Object> requestBody = Map.of(
                "model", claudeModel,
                "max_tokens", maxTokens,
                "messages", new Object[]{
                    Map.of(
                        "role", "user",
                        "content", prompt
                    )
                }
            );

            ClaudeApiResponse response = webClient
                    .post()
                    .uri(claudeApiBaseUrl + "/v1/messages")
                    .header(HttpHeaders.AUTHORIZATION, "Bearer " + claudeApiKey)
                    .header("anthropic-version", "2023-06-01")
                    .contentType(MediaType.APPLICATION_JSON)
                    .bodyValue(requestBody)
                    .retrieve()
                    .bodyToMono(ClaudeApiResponse.class)
                    .timeout(Duration.ofSeconds(30))
                    .block();

            if (response == null || response.getContent() == null || response.getContent().length == 0) {
                throw new BusinessException(ErrorCode.AI_SERVICE_UNAVAILABLE);
            }

            String generatedTip = response.getContent()[0].getText();
            
            // 100자 제한 적용
            if (generatedTip.length() > 100) {
                generatedTip = generatedTip.substring(0, 97) + "...";
            }

            log.debug("AI 마케팅 팁 생성 완료: length={}", generatedTip.length());
            return generatedTip;

        } catch (WebClientResponseException e) {
            log.error("Claude AI API 호출 실패: status={}", e.getStatusCode(), e);
            return generateFallbackTip(storeData, weatherData);
        } catch (Exception e) {
            log.error("AI 마케팅 팁 생성 중 오류 발생", e);
            return generateFallbackTip(storeData, weatherData);
        }
    }

    /**
     * AI 프롬프트 구성
     * 
     * @param storeData 매장 데이터
     * @param weatherData 날씨 데이터
     * @return 프롬프트 문자열
     */
    private String buildPrompt(StoreData storeData, WeatherData weatherData) {
        return String.format(
            "다음 매장을 위한 오늘의 마케팅 팁을 100자 이내로 작성해주세요.\n\n" +
            "매장 정보:\n" +
            "- 매장명: %s\n" +
            "- 업종: %s\n" +
            "- 위치: %s\n\n" +
            "오늘 날씨:\n" +
            "- 온도: %.1f도\n" +
            "- 날씨: %s\n" +
            "- 습도: %.1f%%\n\n" +
            "날씨와 매장 특성을 고려한 실용적이고 구체적인 마케팅 팁을 제안해주세요. " +
            "반드시 100자 이내로 작성하고, 친근하고 실행 가능한 조언을 해주세요.",
            storeData.getStoreName(),
            storeData.getBusinessType(),
            storeData.getLocation(),
            weatherData.getTemperature(),
            weatherData.getCondition(),
            weatherData.getHumidity()
        );
    }

    /**
     * AI API 실패 시 대체 팁 생성
     * 
     * @param storeData 매장 데이터
     * @param weatherData 날씨 데이터
     * @return 대체 마케팅 팁
     */
    private String generateFallbackTip(StoreData storeData, WeatherData weatherData) {
        StringBuilder tip = new StringBuilder();
        
        // 날씨 기반 기본 팁
        if (weatherData.getTemperature() >= 25) {
            tip.append("더운 날씨에는 시원한 음료나 디저트를 홍보해보세요! ");
        } else if (weatherData.getTemperature() <= 10) {
            tip.append("추운 날씨에는 따뜻한 메뉴를 강조해보세요! ");
        } else {
            tip.append("좋은 날씨를 활용한 야외석 이용을 추천해보세요! ");
        }
        
        // 업종별 기본 팁
        String businessCategory = storeData.getBusinessCategory();
        switch (businessCategory) {
            case "카페":
                tip.append("인스타그램용 예쁜 음료 사진을 올려보세요.");
                break;
            case "음식점":
                tip.append("시그니처 메뉴의 맛있는 사진을 SNS에 공유해보세요.");
                break;
            default:
                tip.append("오늘의 특별 메뉴를 SNS에 홍보해보세요.");
                break;
        }
        
        String fallbackTip = tip.toString();
        return fallbackTip.length() > 100 ? fallbackTip.substring(0, 97) + "..." : fallbackTip;
    }

    /**
     * Claude API 응답 DTO
     */
    private static class ClaudeApiResponse {
        private Content[] content;

        public Content[] getContent() { return content; }
        public void setContent(Content[] content) { this.content = content; }

        static class Content {
            private String text;
            private String type;

            public String getText() { return text; }
            public void setText(String text) { this.text = text; }
            public String getType() { return type; }
            public void setType(String type) { this.type = type; }
        }
    }
}/model/MarketingTip.java
package com.won.smarketing.recommend.domain.model;

import lombok.*;

import java.time.LocalDateTime;

/**
 * 마케팅 팁 도메인 모델
 * AI가 생성한 마케팅 팁과 관련 정보를 관리
 */
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
@Builder
public class MarketingTip {

    /**
     * 마케팅 팁 고유 식별자
     */
    private TipId id;

    /**
     * 매장 ID
     */
    private Long storeId;

    /**
     * AI가 생성한 마케팅 팁 내용
     */
    private String tipContent;

    /**
     * 팁 생성 시 참고한 날씨 데이터
     */
    private WeatherData weatherData;

    /**
     * 팁 생성 시 참고한 매장 데이터
     */
    private StoreData storeData;

    /**
     * 팁 생성 시각
     */
    private LocalDateTime createdAt;

    /**
     * 팁 내용 업데이트
     * 
     * @param newContent 새로운 팁 내용
     */
    public void updateContent(String newContent) {
        if (newContent == null || newContent.trim().isEmpty()) {
            throw new IllegalArgumentException("팁 내용은 비어있을 수 없습니다.");
        }
        this.tipContent = newContent.trim();
    }
}
