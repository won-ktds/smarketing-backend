// marketing-content/src/main/java/com/won/smarketing/content/infrastructure/external/ClaudeAiContentGenerator.java
package com.won.smarketing.content.infrastructure.external;

// 수정: domain 패키지의 인터페이스를 import
import com.won.smarketing.content.domain.service.AiContentGenerator;
import com.won.smarketing.content.domain.model.Platform;
import com.won.smarketing.content.presentation.dto.SnsContentCreateRequest;
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
     */
    @Override
    public String generateSnsContent(SnsContentCreateRequest request) {
        try {
            String prompt = buildContentPrompt(request);
            return generateDummySnsContent(request.getTitle(), Platform.fromString(request.getPlatform()));
        } catch (Exception e) {
            log.error("AI 콘텐츠 생성 실패: {}", e.getMessage(), e);
            return generateFallbackContent(request.getTitle(), Platform.fromString(request.getPlatform()));
        }
    }

    /**
     * 플랫폼별 해시태그 생성
     */
    @Override
    public List<String> generateHashtags(String content, Platform platform) {
        try {
            return generateDummyHashtags(platform);
        } catch (Exception e) {
            log.error("해시태그 생성 실패: {}", e.getMessage(), e);
            return generateFallbackHashtags();
        }
    }

    private String buildContentPrompt(SnsContentCreateRequest request) {
        StringBuilder prompt = new StringBuilder();
        prompt.append("제목: ").append(request.getTitle()).append("\n");
        prompt.append("카테고리: ").append(request.getCategory()).append("\n");
        prompt.append("플랫폼: ").append(request.getPlatform()).append("\n");

        if (request.getRequirement() != null) {
            prompt.append("요구사항: ").append(request.getRequirement()).append("\n");
        }

        if (request.getToneAndManner() != null) {
            prompt.append("톤앤매너: ").append(request.getToneAndManner()).append("\n");
        }

        return prompt.toString();
    }

    private String generateDummySnsContent(String title, Platform platform) {
        String baseContent = "🌟 " + title + "를 소개합니다! 🌟\n\n" +
                "저희 매장에서 특별한 경험을 만나보세요.\n" +
                "고객 여러분의 소중한 시간을 더욱 특별하게 만들어드리겠습니다.\n\n";

        if (platform == Platform.INSTAGRAM) {
            return baseContent + "더 많은 정보는 프로필 링크에서 확인하세요! 📸";
        } else {
            return baseContent + "자세한 내용은 저희 블로그를 방문해 주세요! ✨";
        }
    }

    private String generateFallbackContent(String title, Platform platform) {
        return title + "에 대한 멋진 콘텐츠입니다. 많은 관심 부탁드립니다!";
    }

    private List<String> generateDummyHashtags(Platform platform) {
        if (platform == Platform.INSTAGRAM) {
            return Arrays.asList("#맛집", "#데일리", "#소상공인", "#추천", "#인스타그램");
        } else {
            return Arrays.asList("#맛집추천", "#블로그", "#리뷰", "#맛있는곳", "#소상공인응원");
        }
    }

    private List<String> generateFallbackHashtags() {
        return Arrays.asList("#소상공인", "#마케팅", "#홍보");
    }
}