package com.won.smarketing.content.infrastructure.external;

import com.won.smarketing.content.domain.service.AiPosterGenerator; // 도메인 인터페이스 import
import com.won.smarketing.content.presentation.dto.PosterContentCreateRequest;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.Duration;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;

/**
 * Claude AI를 활용한 포스터 생성 구현체
 * Clean Architecture의 Infrastructure Layer에 위치
 */
@Component
@RequiredArgsConstructor
@Slf4j
public class PythonAiPosterGenerator implements AiPosterGenerator {

    private final WebClient webClient;

    @Value("${external.ai-service.base-url:http://20.249.139.88:5001}")
    private String aiServiceBaseUrl;

    /**
     * 포스터 생성 - Python AI 서비스 호출
     *
     * @param request 포스터 생성 요청
     * @return 생성된 포스터 이미지 URL
     */
    @Override
    public String generatePoster(PosterContentCreateRequest request) {
        try {
            log.info("Python AI 포스터 서비스 호출: {}/api/ai/poster", aiServiceBaseUrl);

            // 요청 데이터 구성
            Map<String, Object> requestBody = buildRequestBody(request);

            log.debug("포스터 생성 요청 데이터: {}", requestBody);

            // Python AI 서비스 호출
            Map<String, Object> response = webClient
                    .post()
                    .uri(aiServiceBaseUrl + "/api/ai/poster")
                    .header("Content-Type", "application/json")
                    .bodyValue(requestBody)
                    .retrieve()
                    .bodyToMono(Map.class)
                    .timeout(Duration.ofSeconds(60)) // 포스터 생성은 시간이 오래 걸릴 수 있음
                    .block();

            // 응답에서 content(이미지 URL) 추출
            if (response != null && response.containsKey("content")) {
                String imageUrl = (String) response.get("content");
                log.info("AI 포스터 생성 성공: imageUrl={}", imageUrl);
                return imageUrl;
            } else {
                log.warn("AI 포스터 생성 응답에 content가 없음: {}", response);
                return generateFallbackPosterUrl(request.getTitle());
            }

        } catch (Exception e) {
            log.error("AI 포스터 생성 실패: {}", e.getMessage(), e);
            return generateFallbackPosterUrl(request.getTitle());
        }
    }

    /**
     * 다양한 사이즈의 포스터 생성 (사용하지 않음)
     * 1개의 이미지만 생성하므로 빈 맵 반환
     *
     * @param baseImage 기본 이미지 URL
     * @return 빈 맵
     */
    @Override
    public Map<String, String> generatePosterSizes(String baseImage) {
        log.info("포스터 사이즈 변환 기능은 사용하지 않음: baseImage={}", baseImage);
        return new HashMap<>();
    }

    /**
     * Python AI 서비스 요청 데이터 구성
     * Python 서비스의 PosterContentGetRequest 모델에 맞춤
     */
    private Map<String, Object> buildRequestBody(PosterContentCreateRequest request) {
        Map<String, Object> requestBody = new HashMap<>();

        // 기본 정보
        requestBody.put("title", request.getTitle());
        requestBody.put("category", request.getCategory());
        requestBody.put("contentType", request.getContentType());

        // 이미지 정보
        if (request.getImages() != null && !request.getImages().isEmpty()) {
            requestBody.put("images", request.getImages());
        }

        // 스타일 정보
        if (request.getPhotoStyle() != null) {
            requestBody.put("photoStyle", request.getPhotoStyle());
        }

        // 요구사항
        if (request.getRequirement() != null) {
            requestBody.put("requirement", request.getRequirement());
        }

        // 톤앤매너
        if (request.getToneAndManner() != null) {
            requestBody.put("toneAndManner", request.getToneAndManner());
        }

        // 감정 강도
        if (request.getEmotionIntensity() != null) {
            requestBody.put("emotionIntensity", request.getEmotionIntensity());
        }

        // 메뉴명
        if (request.getMenuName() != null) {
            requestBody.put("menuName", request.getMenuName());
        }

        // 이벤트 정보
        if (request.getEventName() != null) {
            requestBody.put("eventName", request.getEventName());
        }

        // 날짜 정보 (LocalDate를 String으로 변환)
        if (request.getStartDate() != null) {
            requestBody.put("startDate", request.getStartDate().format(DateTimeFormatter.ISO_LOCAL_DATE));
        }

        if (request.getEndDate() != null) {
            requestBody.put("endDate", request.getEndDate().format(DateTimeFormatter.ISO_LOCAL_DATE));
        }

        return requestBody;
    }

    /**
     * 폴백 포스터 URL 생성
     */
    private String generateFallbackPosterUrl(String title) {
        // 기본 포스터 템플릿 URL 반환
        return "https://stdigitalgarage02.blob.core.windows.net/ai-content/fallback-poster.jpg";
    }
}