// marketing-content/src/main/java/com/won/smarketing/content/infrastructure/external/AiContentGenerator.java
package com.won.smarketing.content.infrastructure.external;

import com.won.smarketing.content.domain.model.Platform;
import com.won.smarketing.content.domain.model.CreationConditions;

import java.util.List;

/**
 * AI 콘텐츠 생성 인터페이스
 * Clean Architecture의 Infrastructure Layer에서 외부 AI 서비스와의 연동 정의
 */
public interface AiContentGenerator {

    /**
     * SNS 콘텐츠 생성
     * @param title 제목
     * @param category 카테고리
     * @param platform 플랫폼
     * @param conditions 생성 조건
     * @return 생성된 콘텐츠 텍스트
     */
    String generateSnsContent(String title, String category, Platform platform, CreationConditions conditions);

    /**
     * 해시태그 생성
     * @param content 콘텐츠 내용
     * @param platform 플랫폼
     * @return 생성된 해시태그 목록
     */
    List<String> generateHashtags(String content, Platform platform);
}