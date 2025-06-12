// marketing-content/src/main/java/com/won/smarketing/content/infrastructure/external/ClaudeAiContentGenerator.java
package com.won.smarketing.content.infrastructure.external;

import com.won.smarketing.content.domain.model.Platform;
import com.won.smarketing.content.domain.model.CreationConditions;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.Arrays;
import java.util.List;

/**
 * Claude AI를 활용한 콘텐츠 생성 구현체
 * Clean Architecture의 Infrastructure Layer에 위치
 */
@Component
@RequiredArgsConstructor
@Slf4j
public class ClaudeAiContentGenerator implements AiContentGenerator {

    /**
     * SNS 콘텐츠 생성
     * Claude AI API를 호출하여 SNS 게시물을 생성합니다.
     *
     * @param title 제목
     * @param category 카테고리
     * @param platform 플랫폼
     * @param conditions 생성 조건
     * @return 생성된 콘텐츠 텍스트
     */
    @Override
    public String generateSnsContent(String title, String category, Platform platform, CreationConditions conditions) {
        try {
            // Claude AI API 호출 로직 (실제 구현에서는 HTTP 클라이언트를 사용)
            String prompt = buildContentPrompt(title, category, platform, conditions);

            // TODO: 실제 Claude AI API 호출
            // 현재는 더미 데이터 반환
            return generateDummySnsContent(title, platform);

        } catch (Exception e) {
            log.error("AI 콘텐츠 생성 실패: {}", e.getMessage(), e);
            return generateFallbackContent(title, platform);
        }
    }

    /**
     * 해시태그 생성
     * 콘텐츠 내용을 분석하여 관련 해시태그를 생성합니다.
     *
     * @param content 콘텐츠 내용
     * @param platform 플랫폼
     * @return 생성된 해시태그 목록
     */
    @Override
    public List<String> generateHashtags(String content, Platform platform) {
        try {
            // TODO: 실제 Claude AI API 호출하여 해시태그 생성
            // 현재는 더미 데이터 반환
            return generateDummyHashtags(platform);

        } catch (Exception e) {
            log.error("해시태그 생성 실패: {}", e.getMessage(), e);
            return Arrays.asList("#맛집", "#신메뉴", "#추천");
        }
    }

    /**
     * AI 프롬프트 생성
     */
    private String buildContentPrompt(String title, String category, Platform platform, CreationConditions conditions) {
        StringBuilder prompt = new StringBuilder();
        prompt.append("다음 조건에 맞는 ").append(platform.getDisplayName()).append(" 게시물을 작성해주세요:\n");
        prompt.append("제목: ").append(title).append("\n");
        prompt.append("카테고리: ").append(category).append("\n");

        if (conditions.getRequirement() != null) {
            prompt.append("요구사항: ").append(conditions.getRequirement()).append("\n");
        }
        if (conditions.getToneAndManner() != null) {
            prompt.append("톤앤매너: ").append(conditions.getToneAndManner()).append("\n");
        }
        if (conditions.getEmotionIntensity() != null) {
            prompt.append("감정 강도: ").append(conditions.getEmotionIntensity()).append("\n");
        }

        return prompt.toString();
    }

    /**
     * 더미 SNS 콘텐츠 생성 (개발용)
     */
    private String generateDummySnsContent(String title, Platform platform) {
        switch (platform) {
            case INSTAGRAM:
                return String.format("🎉 %s\n\n맛있는 순간을 놓치지 마세요! 새로운 맛의 경험이 여러분을 기다리고 있어요. 따뜻한 분위기에서 즐기는 특별한 시간을 만들어보세요.\n\n📍 지금 바로 방문해보세요!", title);
            case NAVER_BLOG:
                return String.format("안녕하세요! 오늘은 %s에 대해 소개해드리려고 해요.\n\n정성스럽게 준비한 새로운 메뉴로 고객 여러분께 더 나은 경험을 선사하고 싶습니다. 많은 관심과 사랑 부탁드려요!", title);
            default:
                return String.format("%s - 새로운 경험을 만나보세요!", title);
        }
    }

    /**
     * 더미 해시태그 생성 (개발용)
     */
    private List<String> generateDummyHashtags(Platform platform) {
        switch (platform) {
            case INSTAGRAM:
                return Arrays.asList("#맛집", "#신메뉴", "#인스타그램", "#데일리", "#추천", "#음식스타그램");
            case NAVER_BLOG:
                return Arrays.asList("#맛집", "#리뷰", "#추천", "#신메뉴", "#블로그");
            default:
                return Arrays.asList("#맛집", "#신메뉴", "#추천");
        }
    }

    /**
     * 폴백 콘텐츠 생성 (AI 서비스 실패 시)
     */
    private String generateFallbackContent(String title, Platform platform) {
        return String.format("🎉 %s\n\n새로운 소식을 전해드립니다. 많은 관심 부탁드려요!", title);
    }
}