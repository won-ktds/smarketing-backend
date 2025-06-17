package com.won.smarketing.content.infrastructure.external;

import com.won.smarketing.content.domain.service.AiContentGenerator;
import com.won.smarketing.content.presentation.dto.SnsContentCreateRequest;
import com.won.smarketing.content.presentation.dto.SnsContentCreateResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpMethod;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.Duration;
import java.util.HashMap;
import java.util.Map;

/**
 * Python AI SNS Content Service를 활용한 콘텐츠 생성 구현체
 */
@Component
@RequiredArgsConstructor
@Slf4j
public class ClaudeAiContentGenerator implements AiContentGenerator {

    private final WebClient webClient;

    @Value("${external.ai-service.base-url:http://20.249.113.247:5001}")
    private String aiServiceBaseUrl;

    /**
     * SNS 콘텐츠 생성 - Python AI 서비스 호출
     */
    @Override
    public String generateSnsContent(SnsContentCreateRequest request) {
        log.info("Python AI 서비스 호출: {}/api/ai/sns", aiServiceBaseUrl);

        // 요청 데이터 구성
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("storeId", request.getStoreId());
        requestBody.put("storeName", request.getStoreName());
        requestBody.put("storeType", request.getStoreType());
        requestBody.put("platform", request.getPlatform());
        requestBody.put("title", request.getTitle());
        requestBody.put("category", request.getCategory());
        requestBody.put("contentType", request.getContentType());
        requestBody.put("requirement", request.getRequirement());

        //requestBody.put("tone_and_manner", request.getToneAndManner());
       // requestBody.put("emotion_intensity", request.getEmotionIntensity());
        requestBody.put("target", request.getTarget());

        requestBody.put("event_name", request.getEventName());
        requestBody.put("start_date", request.getStartDate());
        requestBody.put("end_date", request.getEndDate());

        requestBody.put("images", request.getImages());

        // Python AI 서비스 호출
        Map<String, Object> response = webClient
                .method(HttpMethod.GET)
                .uri(aiServiceBaseUrl + "/api/ai/sns")
                .header("Content-Type", "application/json")
                .bodyValue(requestBody)
                .retrieve()
                .bodyToMono(Map.class)
                .timeout(Duration.ofSeconds(30))
                .block();

        String content = "";

        // 응답에서 content 추출
        if (response != null && response.containsKey("content")) {
            content = (String) response.get("content");
            log.info("AI 서비스 응답 성공: contentLength={}", content.length());

            return content;
        }
        return content;
//        } catch (Exception e) {
//            log.error("AI 서비스 호출 실패: {}", e.getMessage(), e);
//            return generateFallbackContent(request.getTitle(), Platform.fromString(request.getPlatform()));
//        }
    }

    /**
     * 폴백 콘텐츠 생성
     */
//    private String generateFallbackContent(String title, Platform platform) {
//        String baseContent = "🌟 " + title + "를 소개합니다! 🌟\n\n" +
//                "저희 매장에서 특별한 경험을 만나보세요.\n" +
//                "고객 여러분의 소중한 시간을 더욱 특별하게 만들어드리겠습니다.\n\n";
//
//        if (platform == Platform.INSTAGRAM) {
//            return baseContent + "더 많은 정보는 프로필 링크에서 확인하세요! 📸";
//        } else {
//            return baseContent + "자세한 내용은 저희 블로그를 방문해 주세요! ✨";
//        }
//    }
}
