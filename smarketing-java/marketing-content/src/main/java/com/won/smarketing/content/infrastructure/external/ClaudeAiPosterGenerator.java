// marketing-content/src/main/java/com/won/smarketing/content/infrastructure/external/ClaudeAiPosterGenerator.java
package com.won.smarketing.content.infrastructure.external;

import com.won.smarketing.content.domain.service.AiPosterGenerator; // 도메인 인터페이스 import
import com.won.smarketing.content.presentation.dto.PosterContentCreateRequest;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.Map;

/**
 * Claude AI를 활용한 포스터 생성 구현체
 * Clean Architecture의 Infrastructure Layer에 위치
 */
@Component
@RequiredArgsConstructor
@Slf4j
public class ClaudeAiPosterGenerator implements AiPosterGenerator {

    /**
     * 포스터 생성
     *
     * @param request 포스터 생성 요청
     * @return 생성된 포스터 이미지 URL
     */
    @Override
    public String generatePoster(PosterContentCreateRequest request) {
        try {
            // Claude AI API 호출 로직
            String prompt = buildPosterPrompt(request);

            // TODO: 실제 Claude AI API 호출
            // 현재는 더미 데이터 반환
            return generateDummyPosterUrl(request.getTitle());

        } catch (Exception e) {
            log.error("AI 포스터 생성 실패: {}", e.getMessage(), e);
            return generateFallbackPosterUrl();
        }
    }

    /**
     * 다양한 사이즈의 포스터 생성
     *
     * @param baseImage 기본 이미지
     * @return 사이즈별 포스터 URL 맵
     */
    @Override
    public Map<String, String> generatePosterSizes(String baseImage) {
        Map<String, String> sizes = new HashMap<>();

        // 다양한 사이즈 생성 (더미 구현)
        sizes.put("instagram_square", baseImage + "_1080x1080.jpg");
        sizes.put("instagram_story", baseImage + "_1080x1920.jpg");
        sizes.put("facebook_post", baseImage + "_1200x630.jpg");
        sizes.put("a4_poster", baseImage + "_2480x3508.jpg");

        return sizes;
    }

    private String buildPosterPrompt(PosterContentCreateRequest request) {
        StringBuilder prompt = new StringBuilder();
        prompt.append("포스터 제목: ").append(request.getTitle()).append("\n");
        prompt.append("카테고리: ").append(request.getCategory()).append("\n");

        if (request.getRequirement() != null) {
            prompt.append("요구사항: ").append(request.getRequirement()).append("\n");
        }

        if (request.getToneAndManner() != null) {
            prompt.append("톤앤매너: ").append(request.getToneAndManner()).append("\n");
        }

        return prompt.toString();
    }

    private String generateDummyPosterUrl(String title) {
        return "https://dummy-ai-service.com/posters/" + title.hashCode() + ".jpg";
    }

    private String generateFallbackPosterUrl() {
        return "https://dummy-ai-service.com/posters/fallback.jpg";
    }
}