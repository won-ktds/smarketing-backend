package com.won.smarketing.content.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

/**
 * SNS 콘텐츠 생성 응답 DTO
 *
 * AI를 통해 SNS 콘텐츠를 생성한 후 클라이언트에게 반환되는 응답 정보입니다.
 * 생성된 콘텐츠의 기본 정보와 함께 사용자가 추가 편집할 수 있는 정보를 포함합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "SNS 콘텐츠 생성 응답")
public class SnsContentCreateResponse {

    // ==================== 기본 식별 정보 ====================

    @Schema(description = "생성된 콘텐츠 ID", example = "1")
    private Long contentId;

    @Schema(description = "콘텐츠 타입", example = "SNS_POST")
    private String contentType;

    @Schema(description = "대상 플랫폼", example = "INSTAGRAM",
            allowableValues = {"INSTAGRAM", "NAVER_BLOG", "FACEBOOK", "KAKAO_STORY"})
    private String platform;

    // ==================== AI 생성 콘텐츠 ====================

    @Schema(description = "AI가 생성한 콘텐츠 제목",
            example = "맛있는 신메뉴를 소개합니다! ✨")
    private String title;

    @Schema(description = "AI가 생성한 콘텐츠 내용",
            example = "안녕하세요! 😊\n\n특별한 신메뉴가 출시되었습니다!\n진짜 맛있어서 꼭 한번 드셔보세요 🍽️\n\n매장에서 기다리고 있을게요! 💫")
    private String content;

    @Schema(description = "AI가 생성한 해시태그 목록",
            example = "[\"맛집\", \"신메뉴\", \"추천\", \"인스타그램\", \"일상\", \"좋아요\", \"팔로우\", \"맛있어요\"]")
    private List<String> hashtags;

    // ==================== 플랫폼별 최적화 정보 ====================

    @Schema(description = "플랫폼별 최적화된 콘텐츠 길이", example = "280")
    private Integer contentLength;

    @Schema(description = "플랫폼별 권장 해시태그 개수", example = "8")
    private Integer recommendedHashtagCount;

    @Schema(description = "플랫폼별 최대 해시태그 개수", example = "15")
    private Integer maxHashtagCount;

    // ==================== 생성 조건 정보 ====================

    @Schema(description = "콘텐츠 생성에 사용된 조건들")
    private GenerationConditionsDto generationConditions;

    // ==================== 상태 및 메타데이터 ====================

    @Schema(description = "생성 상태", example = "DRAFT",
            allowableValues = {"DRAFT", "PUBLISHED", "SCHEDULED"})
    private String status;

    @Schema(description = "생성 일시", example = "2024-01-15T10:30:00")
    private LocalDateTime createdAt;

    @Schema(description = "AI 모델 버전", example = "gpt-4-turbo")
    private String aiModelVersion;

    @Schema(description = "생성 시간 (초)", example = "3.5")
    private Double generationTimeSeconds;

    // ==================== 추가 정보 ====================

    @Schema(description = "업로드된 원본 이미지 URL 목록")
    private List<String> originalImages;

    @Schema(description = "콘텐츠 품질 점수 (1-100)", example = "85")
    private Integer qualityScore;

    @Schema(description = "예상 참여율 (%)", example = "12.5")
    private Double expectedEngagementRate;

    @Schema(description = "콘텐츠 카테고리", example = "음식/메뉴소개")
    private String category;

    // ==================== 편집 가능 여부 ====================

    @Schema(description = "제목 편집 가능 여부", example = "true")
    @Builder.Default
    private Boolean titleEditable = true;

    @Schema(description = "내용 편집 가능 여부", example = "true")
    @Builder.Default
    private Boolean contentEditable = true;

    @Schema(description = "해시태그 편집 가능 여부", example = "true")
    @Builder.Default
    private Boolean hashtagsEditable = true;

    // ==================== 대안 콘텐츠 ====================

    @Schema(description = "대안 제목 목록 (사용자 선택용)")
    private List<String> alternativeTitles;

    @Schema(description = "대안 해시태그 세트 목록")
    private List<List<String>> alternativeHashtagSets;

    // ==================== 내부 DTO 클래스 ====================

    /**
     * 콘텐츠 생성 조건 DTO
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "콘텐츠 생성 조건")
    public static class GenerationConditionsDto {

        @Schema(description = "홍보 대상", example = "메뉴")
        private String targetAudience;

        @Schema(description = "이벤트명", example = "신메뉴 출시 이벤트")
        private String eventName;

        @Schema(description = "톤앤매너", example = "친근함")
        private String toneAndManner;

        @Schema(description = "프로모션 유형", example = "할인 정보")
        private String promotionType;

        @Schema(description = "감정 강도", example = "보통")
        private String emotionIntensity;

        @Schema(description = "홍보 시작일", example = "2024-01-15T09:00:00")
        private LocalDateTime promotionStartDate;

        @Schema(description = "홍보 종료일", example = "2024-01-22T23:59:59")
        private LocalDateTime promotionEndDate;
    }

    // ==================== 비즈니스 메서드 ====================

    /**
     * 플랫폼별 콘텐츠 최적화 여부 확인
     *
     * @return 콘텐츠가 플랫폼 권장 사항을 만족하면 true
     */
    public boolean isOptimizedForPlatform() {
        if (content == null || hashtags == null) {
            return false;
        }

        // 플랫폼별 최적화 기준
        switch (platform.toUpperCase()) {
            case "INSTAGRAM":
                return content.length() <= 2200 &&
                        hashtags.size() <= 15 &&
                        hashtags.size() >= 5;
            case "NAVER_BLOG":
                return content.length() >= 300 &&
                        hashtags.size() <= 10 &&
                        hashtags.size() >= 3;
            case "FACEBOOK":
                return content.length() <= 500 &&
                        hashtags.size() <= 5;
            default:
                return true;
        }
    }

    /**
     * 고품질 콘텐츠 여부 확인
     *
     * @return 품질 점수가 80점 이상이면 true
     */
    public boolean isHighQuality() {
        return qualityScore != null && qualityScore >= 80;
    }

    /**
     * 참여율 예상 등급 반환
     *
     * @return 예상 참여율 등급 (HIGH, MEDIUM, LOW)
     */
    public String getExpectedEngagementLevel() {
        if (expectedEngagementRate == null) {
            return "UNKNOWN";
        }

        if (expectedEngagementRate >= 15.0) {
            return "HIGH";
        } else if (expectedEngagementRate >= 8.0) {
            return "MEDIUM";
        } else {
            return "LOW";
        }
    }

    /**
     * 해시태그를 문자열로 변환 (# 포함)
     *
     * @return #으로 시작하는 해시태그 문자열
     */
    public String getHashtagsAsString() {
        if (hashtags == null || hashtags.isEmpty()) {
            return "";
        }

        return hashtags.stream()
                .map(tag -> "#" + tag)
                .reduce((a, b) -> a + " " + b)
                .orElse("");
    }

    /**
     * 콘텐츠 요약 생성
     *
     * @param maxLength 최대 길이
     * @return 요약된 콘텐츠
     */
    public String getContentSummary(int maxLength) {
        if (content == null || content.length() <= maxLength) {
            return content;
        }
        return content.substring(0, maxLength) + "...";
    }

    /**
     * 플랫폼별 최적화 제안사항 반환
     *
     * @return 최적화 제안사항 목록
     */
    public List<String> getOptimizationSuggestions() {
        List<String> suggestions = new java.util.ArrayList<>();

        if (!isOptimizedForPlatform()) {
            switch (platform.toUpperCase()) {
                case "INSTAGRAM":
                    if (content != null && content.length() > 2200) {
                        suggestions.add("콘텐츠 길이를 2200자 이하로 줄여주세요.");
                    }
                    if (hashtags != null && hashtags.size() > 15) {
                        suggestions.add("해시태그를 15개 이하로 줄여주세요.");
                    }
                    if (hashtags != null && hashtags.size() < 5) {
                        suggestions.add("해시태그를 5개 이상 추가해주세요.");
                    }
                    break;
                case "NAVER_BLOG":
                    if (content != null && content.length() < 300) {
                        suggestions.add("블로그 포스팅을 위해 내용을 300자 이상으로 늘려주세요.");
                    }
                    if (hashtags != null && hashtags.size() > 10) {
                        suggestions.add("네이버 블로그는 해시태그를 10개 이하로 사용하는 것이 좋습니다.");
                    }
                    break;
                case "FACEBOOK":
                    if (content != null && content.length() > 500) {
                        suggestions.add("페이스북에서는 500자 이하의 짧은 글이 더 효과적입니다.");
                    }
                    break;
            }
        }

        return suggestions;
    }

    // ==================== 팩토리 메서드 ====================

    /**
     * 도메인 엔티티에서 SnsContentCreateResponse 생성
     *
     * @param content 콘텐츠 도메인 엔티티
     * @param aiMetadata AI 생성 메타데이터
     * @return SnsContentCreateResponse
     */
    public static SnsContentCreateResponse fromDomain(
            com.won.smarketing.content.domain.model.Content content,
            AiGenerationMetadata aiMetadata) {

        SnsContentCreateResponseBuilder builder = SnsContentCreateResponse.builder()
                .contentId(content.getId())
                .contentType(content.getContentType().name())
                .platform(content.getPlatform().name())
                .title(content.getTitle())
                .content(content.getContent())
                .hashtags(content.getHashtags())
                .status(content.getStatus().name())
                .createdAt(content.getCreatedAt())
                .originalImages(content.getImages());

        // 생성 조건 정보 설정
        if (content.getCreationConditions() != null) {
            builder.generationConditions(GenerationConditionsDto.builder()
                    .targetAudience(content.getCreationConditions().getTargetAudience())
                    .eventName(content.getCreationConditions().getEventName())
                    .toneAndManner(content.getCreationConditions().getToneAndManner())
                    .promotionType(content.getCreationConditions().getPromotionType())
                    .emotionIntensity(content.getCreationConditions().getEmotionIntensity())
                    .promotionStartDate(content.getPromotionStartDate())
                    .promotionEndDate(content.getPromotionEndDate())
                    .build());
        }

        // AI 메타데이터 설정
        if (aiMetadata != null) {
            builder.aiModelVersion(aiMetadata.getModelVersion())
                    .generationTimeSeconds(aiMetadata.getGenerationTime())
                    .qualityScore(aiMetadata.getQualityScore())
                    .expectedEngagementRate(aiMetadata.getExpectedEngagementRate())
                    .alternativeTitles(aiMetadata.getAlternativeTitles())
                    .alternativeHashtagSets(aiMetadata.getAlternativeHashtagSets());
        }

        // 플랫폼별 최적화 정보 설정
        SnsContentCreateResponse response = builder.build();
        response.setContentLength(response.getContent() != null ? response.getContent().length() : 0);
        response.setRecommendedHashtagCount(getRecommendedHashtagCount(content.getPlatform().name()));
        response.setMaxHashtagCount(getMaxHashtagCount(content.getPlatform().name()));

        return response;
    }

    /**
     * 플랫폼별 권장 해시태그 개수 반환
     */
    private static Integer getRecommendedHashtagCount(String platform) {
        switch (platform.toUpperCase()) {
            case "INSTAGRAM": return 8;
            case "NAVER_BLOG": return 5;
            case "FACEBOOK": return 3;
            case "KAKAO_STORY": return 5;
            default: return 5;
        }
    }

    /**
     * 플랫폼별 최대 해시태그 개수 반환
     */
    private static Integer getMaxHashtagCount(String platform) {
        switch (platform.toUpperCase()) {
            case "INSTAGRAM": return 15;
            case "NAVER_BLOG": return 10;
            case "FACEBOOK": return 5;
            case "KAKAO_STORY": return 8;
            default: return 10;
        }
    }

    // ==================== AI 생성 메타데이터 DTO ====================

    /**
     * AI 생성 메타데이터
     * AI 생성 과정에서 나온 부가 정보들
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class AiGenerationMetadata {
        private String modelVersion;
        private Double generationTime;
        private Integer qualityScore;
        private Double expectedEngagementRate;
        private List<String> alternativeTitles;
        private List<List<String>> alternativeHashtagSets;
        private String category;
    }
}