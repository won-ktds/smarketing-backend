// marketing-content/src/main/java/com/won/smarketing/content/infrastructure/external/AiPosterGenerator.java
package com.won.smarketing.content.infrastructure.external;

import com.won.smarketing.content.domain.model.CreationConditions;

import java.util.Map;

/**
 * AI 포스터 생성 인터페이스
 * Clean Architecture의 Infrastructure Layer에서 외부 AI 서비스와의 연동 정의
 */
public interface AiPosterGenerator {

    /**
     * 포스터 이미지 생성
     * @param title 제목
     * @param category 카테고리
     * @param conditions 생성 조건
     * @return 생성된 포스터 이미지 URL
     */
    String generatePoster(String title, String category, CreationConditions conditions);

    /**
     * 포스터 다양한 사이즈 생성
     * @param originalImage 원본 이미지 URL
     * @return 사이즈별 이미지 URL 맵
     */
    Map<String, String> generatePosterSizes(String originalImage);
}