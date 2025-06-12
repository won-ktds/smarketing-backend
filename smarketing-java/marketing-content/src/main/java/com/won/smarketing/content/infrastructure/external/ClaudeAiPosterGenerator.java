// marketing-content/src/main/java/com/won/smarketing/content/infrastructure/external/ClaudeAiPosterGenerator.java
package com.won.smarketing.content.infrastructure.external;

import com.won.smarketing.content.domain.model.CreationConditions;
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
     * 포스터 이미지 생성
     * Claude AI API를 호출하여 홍보 포스터를 생성합니다.
     *
     * @param title 제목
     * @param category 카테고리
     * @param conditions 생성 조건
     * @return 생성된 포스터 이미지 URL
     */
    @Override
    public String generatePoster(String title, String category, CreationConditions conditions) {
        try {
            // Claude AI API 호출 로직 (실제 구현에서는 HTTP 클라이언트를 사용)
            String prompt = buildPosterPrompt(title, category, conditions);

            // TODO: 실제 Claude AI API 호출
            // 현재는 더미 데이터 반환
            return generateDummyPosterUrl(title);

        } catch (Exception e) {
            log.error("AI 포스터 생성 실패: {}", e.getMessage(), e);
            return generateFallbackPosterUrl();
        }
    }

    /**
     * 포스터 다양한 사이즈 생성
     * 원본 포스터를 기반으로 다양한 사이즈의 포스터를 생성합니다.
     *
     * @param originalImage 원본 이미지 URL
     * @return 사이즈별 이미지 URL 맵
     */
    @Override
    public Map<String, String> generatePosterSizes(String originalImage) {
        try {
            // TODO: 실제 이미지 리사이징 API 호출
            // 현재는 더미 데이터 반환
            return generateDummyPosterSizes(originalImage);

        } catch (Exception e) {
            log.error("포스터 사이즈 생성 실패: {}", e.getMessage(), e);
            return new HashMap<>();
        }
    }

    /**
     * AI 포스터 프롬프트 생성
     */
    private String buildPosterPrompt(String title, String category, CreationConditions conditions) {
        StringBuilder prompt = new StringBuilder();
        prompt.append("다음 조건에 맞는 홍보 포스터를 생성해주세요:\n");
        prompt.append("제목: ").append(title).append("\n");
        prompt.append("카테고리: ").append(category).append("\n");

        if (conditions.getPhotoStyle() != null) {
            prompt.append("사진 스타일: ").append(conditions.getPhotoStyle()).append("\n");
        }
        if (conditions.getRequirement() != null) {
            prompt.append("요구사항: ").append(conditions.getRequirement()).append("\n");
        }
        if (conditions.getToneAndManner() != null) {
            prompt.append("톤앤매너: ").append(conditions.getToneAndManner()).append("\n");
        }

        return prompt.toString();
    }

    /**
     * 더미 포스터 URL 생성 (개발용)
     */
    private String generateDummyPosterUrl(String title) {
        return String.format("https://example.com/posters/%s-poster.jpg",
                title.replaceAll("\\s+", "-").toLowerCase());
    }

    /**
     * 더미 포스터 사이즈별 URL 생성 (개발용)
     */
    private Map<String, String> generateDummyPosterSizes(String originalImage) {
        Map<String, String> sizes = new HashMap<>();
        String baseUrl = originalImage.substring(0, originalImage.lastIndexOf("."));
        String extension = originalImage.substring(originalImage.lastIndexOf("."));

        sizes.put("small", baseUrl + "-small" + extension);
        sizes.put("medium", baseUrl + "-medium" + extension);
        sizes.put("large", baseUrl + "-large" + extension);
        sizes.put("xlarge", baseUrl + "-xlarge" + extension);

        return sizes;
    }

    /**
     * 폴백 포스터 URL 생성 (AI 서비스 실패 시)
     */
    private String generateFallbackPosterUrl() {
        return "https://example.com/posters/default-poster.jpg";
    }
}