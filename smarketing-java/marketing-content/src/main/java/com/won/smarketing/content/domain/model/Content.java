// marketing-content/src/main/java/com/won/smarketing/content/domain/model/Content.java
package com.won.smarketing.content.domain.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * 콘텐츠 도메인 모델
 *
 * 이 클래스는 마케팅 콘텐츠의 핵심 정보와 비즈니스 로직을 포함하는 
 * DDD(Domain-Driven Design) 엔티티입니다.
 *
 * Clean Architecture의 Domain Layer에 위치하며,
 * 비즈니스 규칙과 도메인 로직을 캡슐화합니다.
 */
@Entity
@Table(
        name = "contents",
        indexes = {
                @Index(name = "idx_store_id", columnList = "store_id"),
                @Index(name = "idx_content_type", columnList = "content_type"),
                @Index(name = "idx_platform", columnList = "platform"),
                @Index(name = "idx_status", columnList = "status"),
                @Index(name = "idx_promotion_dates", columnList = "promotion_start_date, promotion_end_date"),
                @Index(name = "idx_created_at", columnList = "created_at")
        }
)
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EntityListeners(AuditingEntityListener.class)
public class Content {

    // ==================== 기본키 및 식별자 ====================

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long id;

    // ==================== 콘텐츠 분류 ====================

    @Enumerated(EnumType.STRING)
    @Column(name = "content_type", nullable = false, length = 20)
    private ContentType contentType;

    @Enumerated(EnumType.STRING)
    @Column(name = "platform", nullable = false, length = 20)
    private Platform platform;

    // ==================== 콘텐츠 내용 ====================

    @Column(name = "title", nullable = false, length = 200)
    private String title;

    @Column(name = "content", nullable = false, columnDefinition = "TEXT")
    private String content;

    // ==================== 멀티미디어 및 메타데이터 ====================

    @ElementCollection(fetch = FetchType.LAZY)
    @CollectionTable(
            name = "content_hashtags",
            joinColumns = @JoinColumn(name = "content_id"),
            indexes = @Index(name = "idx_content_hashtags", columnList = "content_id")
    )
    @Column(name = "hashtag", length = 100)
    @Builder.Default
    private List<String> hashtags = new ArrayList<>();

    @ElementCollection(fetch = FetchType.LAZY)
    @CollectionTable(
            name = "content_images",
            joinColumns = @JoinColumn(name = "content_id"),
            indexes = @Index(name = "idx_content_images", columnList = "content_id")
    )
    @Column(name = "image_url", length = 500)
    @Builder.Default
    private List<String> images = new ArrayList<>();

    // ==================== 상태 관리 ====================

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, length = 20)
    @Builder.Default
    private ContentStatus status = ContentStatus.DRAFT;

    // ==================== AI 생성 조건 (Embedded) ====================
    //@Embedded
    @AttributeOverrides({
            @AttributeOverride(name = "toneAndManner", column = @Column(name = "tone_and_manner", length = 50)),
            @AttributeOverride(name = "promotionType", column = @Column(name = "promotion_type", length = 50)),
            @AttributeOverride(name = "emotionIntensity", column = @Column(name = "emotion_intensity", length = 50)),
            @AttributeOverride(name = "targetAudience", column = @Column(name = "target_audience", length = 50)),
            @AttributeOverride(name = "eventName", column = @Column(name = "event_name", length = 100))
    })
    private CreationConditions creationConditions;

    // ==================== 비즈니스 관계 ====================

    @Column(name = "store_id", nullable = false)
    private Long storeId;

    // ==================== 홍보 기간 ====================

    @Column(name = "promotion_start_date")
    private LocalDateTime promotionStartDate;

    @Column(name = "promotion_end_date")
    private LocalDateTime promotionEndDate;

    // ==================== 감사(Audit) 정보 ====================

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    public Content(ContentId of, ContentType contentType, Platform platform, String title, String content, List<String> strings, List<String> strings1, ContentStatus contentStatus, CreationConditions conditions, Long storeId, LocalDateTime createdAt, LocalDateTime updatedAt) {
    }

    // ==================== 비즈니스 로직 메서드 ====================

    /**
     * 콘텐츠 제목 수정
     *
     * 비즈니스 규칙:
     * - 제목은 null이거나 빈 값일 수 없음
     * - 200자를 초과할 수 없음
     * - 발행된 콘텐츠는 제목 변경 시 상태가 DRAFT로 변경됨
     *
     * @param title 새로운 제목
     * @throws IllegalArgumentException 제목이 유효하지 않은 경우
     */
    public void updateTitle(String title) {
        validateTitle(title);

        boolean wasPublished = isPublished();
        this.title = title.trim();

        // 발행된 콘텐츠의 제목이 변경되면 재검토 필요
        if (wasPublished) {
            this.status = ContentStatus.DRAFT;
        }
    }

    /**
     * 콘텐츠 내용 수정
     *
     * 비즈니스 규칙:
     * - 내용은 null이거나 빈 값일 수 없음
     * - 발행된 콘텐츠는 내용 변경 시 상태가 DRAFT로 변경됨
     *
     * @param content 새로운 콘텐츠 내용
     * @throws IllegalArgumentException 내용이 유효하지 않은 경우
     */
    public void updateContent(String content) {
        validateContent(content);

        boolean wasPublished = isPublished();
        this.content = content.trim();

        // 발행된 콘텐츠의 내용이 변경되면 재검토 필요
        if (wasPublished) {
            this.status = ContentStatus.DRAFT;
        }
    }

    /**
     * 콘텐츠 상태 변경
     *
     * 비즈니스 규칙:
     * - PUBLISHED 상태로 변경시 유효성 검증 수행
     * - ARCHIVED 상태에서는 PUBLISHED로만 변경 가능
     *
     * @param status 새로운 상태
     * @throws IllegalStateException 잘못된 상태 전환인 경우
     */
//    public void changeStatus(ContentStatus status) {
//        validateStatusTransition(this.status, status);
//
//        if (status == ContentStatus.PUBLISHED) {
//            validateForPublication();
//        }
//
//        this.status = status;
//    }

    /**
     * 홍보 기간 설정
     *
     * 비즈니스 규칙:
     * - 시작일은 종료일보다 이전이어야 함
     * - 과거 날짜로 설정 불가 (현재 시간 기준)
     *
     * @param startDate 홍보 시작일
     * @param endDate 홍보 종료일
     * @throws IllegalArgumentException 날짜가 유효하지 않은 경우
     */
    public void setPromotionPeriod(LocalDateTime startDate, LocalDateTime endDate) {
        validatePromotionPeriod(startDate, endDate);

        this.promotionStartDate = startDate;
        this.promotionEndDate = endDate;
    }

    /**
     * 홍보 기간 설정
     *
     * 비즈니스 규칙:
     * - 시작일은 종료일보다 이전이어야 함
     * - 과거 날짜로 설정 불가 (현재 시간 기준)
     *
     * @param startDate 홍보 시작일
     * @param endDate 홍보 종료일
     * @throws IllegalArgumentException 날짜가 유효하지 않은 경우
     */
    public void updatePeriod(LocalDateTime startDate, LocalDateTime endDate) {
        validatePromotionPeriod(startDate, endDate);

        this.promotionStartDate = startDate;
        this.promotionEndDate = endDate;
    }

    /**
     * 해시태그 추가
     *
     * @param hashtag 추가할 해시태그 (# 없이)
     */
    public void addHashtag(String hashtag) {
        if (hashtag != null && !hashtag.trim().isEmpty()) {
            String cleanHashtag = hashtag.trim().replace("#", "");
            if (!this.hashtags.contains(cleanHashtag)) {
                this.hashtags.add(cleanHashtag);
            }
        }
    }

    /**
     * 해시태그 제거
     *
     * @param hashtag 제거할 해시태그
     */
    public void removeHashtag(String hashtag) {
        if (hashtag != null) {
            String cleanHashtag = hashtag.trim().replace("#", "");
            this.hashtags.remove(cleanHashtag);
        }
    }

    /**
     * 이미지 추가
     *
     * @param imageUrl 이미지 URL
     */
    public void addImage(String imageUrl) {
        if (imageUrl != null && !imageUrl.trim().isEmpty()) {
            if (!this.images.contains(imageUrl.trim())) {
                this.images.add(imageUrl.trim());
            }
        }
    }

    /**
     * 이미지 제거
     *
     * @param imageUrl 제거할 이미지 URL
     */
    public void removeImage(String imageUrl) {
        if (imageUrl != null) {
            this.images.remove(imageUrl.trim());
        }
    }

    // ==================== 도메인 조회 메서드 ====================

    /**
     * 발행 상태 확인
     *
     * @return 발행된 상태이면 true
     */
    public boolean isPublished() {
        return this.status == ContentStatus.PUBLISHED;
    }

    /**
     * 수정 가능 상태 확인
     *
     * @return 임시저장 또는 예약발행 상태이면 true
     */
    public boolean isEditable() {
        return this.status == ContentStatus.DRAFT || this.status == ContentStatus.PUBLISHED;
    }

    /**
     * 현재 홍보 진행 중인지 확인
     *
     * @return 홍보 기간 내이고 발행 상태이면 true
     */
    public boolean isOngoingPromotion() {
        if (!isPublished() || promotionStartDate == null || promotionEndDate == null) {
            return false;
        }

        LocalDateTime now = LocalDateTime.now();
        return now.isAfter(promotionStartDate) && now.isBefore(promotionEndDate);
    }

    /**
     * 홍보 예정 상태 확인
     *
     * @return 홍보 시작 전이면 true
     */
    public boolean isUpcomingPromotion() {
        if (promotionStartDate == null) {
            return false;
        }

        return LocalDateTime.now().isBefore(promotionStartDate);
    }

    /**
     * 홍보 완료 상태 확인
     *
     * @return 홍보 종료 후이면 true
     */
    public boolean isCompletedPromotion() {
        if (promotionEndDate == null) {
            return false;
        }

        return LocalDateTime.now().isAfter(promotionEndDate);
    }

    /**
     * SNS 콘텐츠 여부 확인
     *
     * @return SNS 게시물이면 true
     */
//    public boolean isSnsContent() {
//        return this.contentType == ContentType.SNS_POST;
//    }

    /**
     * 포스터 콘텐츠 여부 확인
     *
     * @return 포스터이면 true
     */
    public boolean isPosterContent() {
        return this.contentType == ContentType.POSTER;
    }

    /**
     * 이미지가 있는 콘텐츠인지 확인
     *
     * @return 이미지가 1개 이상 있으면 true
     */
    public boolean hasImages() {
        return this.images != null && !this.images.isEmpty();
    }

    /**
     * 해시태그가 있는 콘텐츠인지 확인
     *
     * @return 해시태그가 1개 이상 있으면 true
     */
    public boolean hasHashtags() {
        return this.hashtags != null && !this.hashtags.isEmpty();
    }

    // ==================== 유효성 검증 메서드 ====================

    /**
     * 제목 유효성 검증
     */
    private void validateTitle(String title) {
        if (title == null || title.trim().isEmpty()) {
            throw new IllegalArgumentException("제목은 필수 입력 사항입니다.");
        }
        if (title.trim().length() > 200) {
            throw new IllegalArgumentException("제목은 200자를 초과할 수 없습니다.");
        }
    }

    /**
     * 내용 유효성 검증
     */
    private void validateContent(String content) {
        if (content == null || content.trim().isEmpty()) {
            throw new IllegalArgumentException("콘텐츠 내용은 필수 입력 사항입니다.");
        }
    }

    /**
     * 홍보 기간 유효성 검증
     */
    private void validatePromotionPeriod(LocalDateTime startDate, LocalDateTime endDate) {
        if (startDate == null || endDate == null) {
            throw new IllegalArgumentException("홍보 시작일과 종료일은 필수 입력 사항입니다.");
        }
        if (startDate.isAfter(endDate)) {
            throw new IllegalArgumentException("홍보 시작일은 종료일보다 이전이어야 합니다.");
        }
        if (endDate.isBefore(LocalDateTime.now())) {
            throw new IllegalArgumentException("홍보 종료일은 현재 시간 이후여야 합니다.");
        }
    }

    /**
     * 상태 전환 유효성 검증
     */
//    private void validateStatusTransition(ContentStatus from, ContentStatus to) {
//        if (from == ContentStatus.ARCHIVED && to != ContentStatus.PUBLISHED) {
//            throw new IllegalStateException("보관된 콘텐츠는 발행 상태로만 변경할 수 있습니다.");
//        }
//    }

    /**
     * 발행을 위한 유효성 검증
     */
    private void validateForPublication() {
        validateTitle(this.title);
        validateContent(this.content);

        if (this.promotionStartDate == null || this.promotionEndDate == null) {
            throw new IllegalStateException("발행하려면 홍보 기간을 설정해야 합니다.");
        }

        if (this.contentType == ContentType.POSTER && !hasImages()) {
            throw new IllegalStateException("포스터 콘텐츠는 이미지가 필수입니다.");
        }
    }

    // ==================== 비즈니스 계산 메서드 ====================

    /**
     * 홍보 진행률 계산 (0-100%)
     *
     * @return 진행률
     */
    public double calculateProgress() {
        if (promotionStartDate == null || promotionEndDate == null) {
            return 0.0;
        }

        LocalDateTime now = LocalDateTime.now();

        if (now.isBefore(promotionStartDate)) {
            return 0.0;
        } else if (now.isAfter(promotionEndDate)) {
            return 100.0;
        }

        long totalDuration = java.time.Duration.between(promotionStartDate, promotionEndDate).toHours();
        long elapsedDuration = java.time.Duration.between(promotionStartDate, now).toHours();

        if (totalDuration == 0) {
            return 100.0;
        }

        return (double) elapsedDuration / totalDuration * 100.0;
    }

    /**
     * 남은 홍보 일수 계산
     *
     * @return 남은 일수 (음수면 0)
     */
    public long calculateRemainingDays() {
        if (promotionEndDate == null) {
            return 0L;
        }

        LocalDateTime now = LocalDateTime.now();
        if (now.isAfter(promotionEndDate)) {
            return 0L;
        }

        return java.time.Duration.between(now, promotionEndDate).toDays();
    }

    // ==================== 팩토리 메서드 ====================

    /**
     * SNS 콘텐츠 생성 팩토리 메서드
     */
    public static Content createSnsContent(String title, String content, Platform platform,
                                           Long storeId, CreationConditions conditions) {
        Content snsContent = Content.builder()
//                .contentType(ContentType.SNS_POST)
                .platform(platform)
                .title(title)
                .content(content)
                .storeId(storeId)
                .creationConditions(conditions)
                .status(ContentStatus.DRAFT)
                .hashtags(new ArrayList<>())
                .images(new ArrayList<>())
                .build();

        // 유효성 검증
        snsContent.validateTitle(title);
        snsContent.validateContent(content);

        return snsContent;
    }

    /**
     * 포스터 콘텐츠 생성 팩토리 메서드
     */
    public static Content createPosterContent(String title, String content, List<String> images,
                                              Long storeId, CreationConditions conditions) {
        if (images == null || images.isEmpty()) {
            throw new IllegalArgumentException("포스터 콘텐츠는 이미지가 필수입니다.");
        }

        Content posterContent = Content.builder()
                .contentType(ContentType.POSTER)
                .platform(Platform.INSTAGRAM) // 기본값
                .title(title)
                .content(content)
                .storeId(storeId)
                .creationConditions(conditions)
                .status(ContentStatus.DRAFT)
                .hashtags(new ArrayList<>())
                .images(new ArrayList<>(images))
                .build();

        // 유효성 검증
        posterContent.validateTitle(title);
        posterContent.validateContent(content);

        return posterContent;
    }

    // ==================== Object 메서드 오버라이드 ====================

    /**
     * 비즈니스 키 기반 동등성 비교
     * JPA 엔티티에서는 ID가 아닌 비즈니스 키 사용 권장
     */
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;

        Content content = (Content) obj;
        return id != null && id.equals(content.id);
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }

    /**
     * 디버깅용 toString (민감한 정보 제외)
     */
    @Override
    public String toString() {
        return "Content{" +
                "id=" + id +
                ", contentType=" + contentType +
                ", platform=" + platform +
                ", title='" + title + '\'' +
                ", status=" + status +
                ", storeId=" + storeId +
                ", promotionStartDate=" + promotionStartDate +
                ", promotionEndDate=" + promotionEndDate +
                ", createdAt=" + createdAt +
                '}';
    }
}

/*
==================== 데이터베이스 스키마 (참고용) ====================

CREATE TABLE contents (
    content_id BIGINT NOT NULL AUTO_INCREMENT,
    content_type VARCHAR(20) NOT NULL,
    platform VARCHAR(20) NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'DRAFT',
    tone_and_manner VARCHAR(50),
    promotion_type VARCHAR(50),
    emotion_intensity VARCHAR(50),
    target_audience VARCHAR(50),
    event_name VARCHAR(100),
    store_id BIGINT NOT NULL,
    promotion_start_date DATETIME,
    promotion_end_date DATETIME,
    created_at DATETIME NOT NULL,
    updated_at DATETIME,
    PRIMARY KEY (content_id),
    INDEX idx_store_id (store_id),
    INDEX idx_content_type (content_type),
    INDEX idx_platform (platform),
    INDEX idx_status (status),
    INDEX idx_promotion_dates (promotion_start_date, promotion_end_date),
    INDEX idx_created_at (created_at)
);

CREATE TABLE content_hashtags (
    content_id BIGINT NOT NULL,
    hashtag VARCHAR(100) NOT NULL,
    INDEX idx_content_hashtags (content_id),
    FOREIGN KEY (content_id) REFERENCES contents(content_id) ON DELETE CASCADE
);

CREATE TABLE content_images (
    content_id BIGINT NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    INDEX idx_content_images (content_id),
    FOREIGN KEY (content_id) REFERENCES contents(content_id) ON DELETE CASCADE
);
*/