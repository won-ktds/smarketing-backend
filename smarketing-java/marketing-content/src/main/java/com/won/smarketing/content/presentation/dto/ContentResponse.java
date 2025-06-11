// marketing-content/src/main/java/com/won/smarketing/content/presentation/dto/ContentResponse.java
package com.won.smarketing.content.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 콘텐츠 응답 DTO
 * 콘텐츠 목록 조회 시 사용되는 기본 응답 DTO
 *
 * 이 클래스는 콘텐츠의 핵심 정보만을 포함하여 목록 조회 시 성능을 최적화합니다.
 * 상세 정보가 필요한 경우 ContentDetailResponse를 사용합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "콘텐츠 응답")
public class ContentResponse {

    // ==================== 기본 식별 정보 ====================

    @Schema(description = "콘텐츠 ID", example = "1")
    private Long contentId;

    @Schema(description = "콘텐츠 타입", example = "SNS_POST",
            allowableValues = {"SNS_POST", "POSTER"})
    private String contentType;

    @Schema(description = "플랫폼", example = "INSTAGRAM",
            allowableValues = {"INSTAGRAM", "NAVER_BLOG", "FACEBOOK", "KAKAO_STORY"})
    private String platform;

    // ==================== 콘텐츠 정보 ====================

    @Schema(description = "제목", example = "맛있는 신메뉴를 소개합니다!")
    private String title;

    @Schema(description = "콘텐츠 내용", example = "특별한 신메뉴가 출시되었습니다! 🍽️\n지금 바로 맛보세요!")
    private String content;

    @Schema(description = "해시태그 목록", example = "[\"#맛집\", \"#신메뉴\", \"#추천\", \"#인스타그램\"]")
    private List<String> hashtags;

    @Schema(description = "이미지 URL 목록",
            example = "[\"https://example.com/image1.jpg\", \"https://example.com/image2.jpg\"]")
    private List<String> images;

    // ==================== 상태 관리 ====================

    @Schema(description = "상태", example = "PUBLISHED",
            allowableValues = {"DRAFT", "PUBLISHED", "SCHEDULED", "ARCHIVED"})
    private String status;

    @Schema(description = "상태 표시명", example = "발행완료")
    private String statusDisplay;

    // ==================== 홍보 기간 ====================

    @Schema(description = "홍보 시작일", example = "2024-01-15T09:00:00")
    private LocalDateTime promotionStartDate;

    @Schema(description = "홍보 종료일", example = "2024-01-22T23:59:59")
    private LocalDateTime promotionEndDate;

    // ==================== 시간 정보 ====================

    @Schema(description = "생성일시", example = "2024-01-15T10:30:00")
    private LocalDateTime createdAt;

    @Schema(description = "수정일시", example = "2024-01-15T14:20:00")
    private LocalDateTime updatedAt;

    // ==================== 계산된 필드들 ====================

    @Schema(description = "홍보 진행 상태", example = "ONGOING",
            allowableValues = {"UPCOMING", "ONGOING", "COMPLETED"})
    private String promotionStatus;

    @Schema(description = "남은 홍보 일수", example = "5")
    private Long remainingDays;

    @Schema(description = "홍보 진행률 (%)", example = "60.5")
    private Double progressPercentage;

    @Schema(description = "콘텐츠 요약 (첫 50자)", example = "특별한 신메뉴가 출시되었습니다! 지금 바로 맛보세요...")
    private String contentSummary;

    @Schema(description = "이미지 개수", example = "3")
    private Integer imageCount;

    @Schema(description = "해시태그 개수", example = "8")
    private Integer hashtagCount;

    @Schema(description = "조회수", example = "8")
    private Integer viewCount;

    // ==================== 비즈니스 메서드 ====================

    /**
     * 콘텐츠 요약 생성
     * 콘텐츠가 길 경우 첫 50자만 표시하고 "..." 추가
     *
     * @param content 원본 콘텐츠
     * @param maxLength 최대 길이
     * @return 요약된 콘텐츠
     */
    public static String createContentSummary(String content, int maxLength) {
        if (content == null || content.length() <= maxLength) {
            return content;
        }
        return content.substring(0, maxLength) + "...";
    }

    /**
     * 홍보 상태 계산
     * 현재 시간과 홍보 기간을 비교하여 상태 결정
     *
     * @param startDate 홍보 시작일
     * @param endDate 홍보 종료일
     * @return 홍보 상태
     */
    public static String calculatePromotionStatus(LocalDateTime startDate, LocalDateTime endDate) {
        if (startDate == null || endDate == null) {
            return "UNKNOWN";
        }

        LocalDateTime now = LocalDateTime.now();

        if (now.isBefore(startDate)) {
            return "UPCOMING";  // 홍보 예정
        } else if (now.isAfter(endDate)) {
            return "COMPLETED"; // 홍보 완료
        } else {
            return "ONGOING";   // 홍보 진행중
        }
    }

    /**
     * 남은 일수 계산
     * 홍보 종료일까지 남은 일수 계산
     *
     * @param endDate 홍보 종료일
     * @return 남은 일수 (음수면 0 반환)
     */
    public static Long calculateRemainingDays(LocalDateTime endDate) {
        if (endDate == null) {
            return 0L;
        }

        LocalDateTime now = LocalDateTime.now();
        if (now.isAfter(endDate)) {
            return 0L;
        }

        return java.time.Duration.between(now, endDate).toDays();
    }

    /**
     * 진행률 계산
     * 홍보 기간 대비 진행률 계산 (0-100%)
     *
     * @param startDate 홍보 시작일
     * @param endDate 홍보 종료일
     * @return 진행률 (0-100%)
     */
    public static Double calculateProgressPercentage(LocalDateTime startDate, LocalDateTime endDate) {
        if (startDate == null || endDate == null) {
            return 0.0;
        }

        LocalDateTime now = LocalDateTime.now();

        if (now.isBefore(startDate)) {
            return 0.0;  // 아직 시작 안함
        } else if (now.isAfter(endDate)) {
            return 100.0; // 완료
        }

        long totalDuration = java.time.Duration.between(startDate, endDate).toHours();
        long elapsedDuration = java.time.Duration.between(startDate, now).toHours();

        if (totalDuration == 0) {
            return 100.0;
        }

        return (double) elapsedDuration / totalDuration * 100.0;
    }

    /**
     * 상태 표시명 변환
     * 영문 상태를 한글로 변환
     *
     * @param status 영문 상태
     * @return 한글 상태명
     */
    public static String getStatusDisplay(String status) {
        if (status == null) {
            return "알 수 없음";
        }

        switch (status) {
            case "DRAFT":
                return "임시저장";
            case "PUBLISHED":
                return "발행완료";
            case "SCHEDULED":
                return "예약발행";
            case "ARCHIVED":
                return "보관됨";
            default:
                return status;
        }
    }

    // ==================== Builder 확장 메서드 ====================

    /**
     * 도메인 엔티티에서 ContentResponse 생성
     * 계산된 필드들을 자동으로 설정
     *
     * @param content 콘텐츠 도메인 엔티티
     * @return ContentResponse
     */
    public static ContentResponse fromDomain(com.won.smarketing.content.domain.model.Content content) {
        ContentResponseBuilder builder = ContentResponse.builder()
                .contentId(content.getId())
                .contentType(content.getContentType().name())
                .platform(content.getPlatform().name())
                .title(content.getTitle())
                .content(content.getContent())
                .hashtags(content.getHashtags())
                .images(content.getImages())
                .status(content.getStatus().name())
                .statusDisplay(getStatusDisplay(content.getStatus().name()))
                .promotionStartDate(content.getPromotionStartDate())
                .promotionEndDate(content.getPromotionEndDate())
                .createdAt(content.getCreatedAt())
                .updatedAt(content.getUpdatedAt());

        // 계산된 필드들 설정
        builder.contentSummary(createContentSummary(content.getContent(), 50));
        builder.imageCount(content.getImages() != null ? content.getImages().size() : 0);
        builder.hashtagCount(content.getHashtags() != null ? content.getHashtags().size() : 0);

        // 홍보 관련 계산 필드들
        builder.promotionStatus(calculatePromotionStatus(
                content.getPromotionStartDate(),
                content.getPromotionEndDate()));
        builder.remainingDays(calculateRemainingDays(content.getPromotionEndDate()));
        builder.progressPercentage(calculateProgressPercentage(
                content.getPromotionStartDate(),
                content.getPromotionEndDate()));

        return builder.build();
    }

    // ==================== 유틸리티 메서드 ====================

    /**
     * 콘텐츠가 현재 활성 상태인지 확인
     *
     * @return 홍보 기간 내이고 발행 상태면 true
     */
    public boolean isActive() {
        return "PUBLISHED".equals(status) && "ONGOING".equals(promotionStatus);
    }

    /**
     * 콘텐츠 수정 가능 여부 확인
     *
     * @return 임시저장 상태이거나 예약발행 상태면 true
     */
    public boolean isEditable() {
        return "DRAFT".equals(status) || "SCHEDULED".equals(status);
    }

    /**
     * 이미지가 있는 콘텐츠인지 확인
     *
     * @return 이미지가 1개 이상 있으면 true
     */
    public boolean hasImages() {
        return images != null && !images.isEmpty();
    }

    /**
     * 해시태그가 있는 콘텐츠인지 확인
     *
     * @return 해시태그가 1개 이상 있으면 true
     */
    public boolean hasHashtags() {
        return hashtags != null && !hashtags.isEmpty();
    }

    /**
     * 디버깅용 toString (간소화된 정보만)
     */
    @Override
    public String toString() {
        return "ContentResponse{" +
                "contentId=" + contentId +
                ", contentType='" + contentType + '\'' +
                ", platform='" + platform + '\'' +
                ", title='" + title + '\'' +
                ", status='" + status + '\'' +
                ", promotionStatus='" + promotionStatus + '\'' +
                ", createdAt=" + createdAt +
                '}';
    }
}

/*
==================== 사용 예시 ====================

// 1. 도메인 엔티티에서 DTO 생성
Content domainContent = contentRepository.findById(contentId);
ContentResponse response = ContentResponse.fromDomain(domainContent);

// 2. 수동으로 빌더 사용
ContentResponse response = ContentResponse.builder()
    .contentId(1L)
    .contentType("SNS_POST")
    .platform("INSTAGRAM")
    .title("맛있는 신메뉴")
    .content("특별한 신메뉴가 출시되었습니다!")
    .status("PUBLISHED")
    .build();

// 3. 비즈니스 로직 활용
boolean canEdit = response.isEditable();
boolean isLive = response.isActive();
String summary = response.getContentSummary();

==================== JSON 응답 예시 ====================

{
  "contentId": 1,
  "contentType": "SNS_POST",
  "platform": "INSTAGRAM",
  "title": "맛있는 신메뉴를 소개합니다!",
  "content": "특별한 신메뉴가 출시되었습니다! 🍽️\n지금 바로 맛보세요!",
  "hashtags": ["#맛집", "#신메뉴", "#추천", "#인스타그램"],
  "images": ["https://example.com/image1.jpg"],
  "status": "PUBLISHED",
  "statusDisplay": "발행완료",
  "promotionStartDate": "2024-01-15T09:00:00",
  "promotionEndDate": "2024-01-22T23:59:59",
  "createdAt": "2024-01-15T10:30:00",
  "updatedAt": "2024-01-15T14:20:00",
  "promotionStatus": "ONGOING",
  "remainingDays": 5,
  "progressPercentage": 60.5,
  "contentSummary": "특별한 신메뉴가 출시되었습니다! 지금 바로 맛보세요...",
  "imageCount": 1,
  "hashtagCount": 4
}
*/