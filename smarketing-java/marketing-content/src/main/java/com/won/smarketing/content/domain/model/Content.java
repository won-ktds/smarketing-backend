// marketing-content/src/main/java/com/won/smarketing/content/domain/model/Content.java
package com.won.smarketing.content.domain.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * 콘텐츠 도메인 모델
 *
 * Clean Architecture의 Domain Layer에 위치하는 핵심 엔티티
 * JPA 애노테이션을 제거하여 순수 도메인 모델로 유지
 * Infrastructure Layer에서 별도의 JPA 엔티티로 매핑
 */
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Content {

    // ==================== 기본키 및 식별자 ====================
    private Long id;

    // ==================== 콘텐츠 분류 ====================
    private ContentType contentType;
    private Platform platform;

    // ==================== 콘텐츠 내용 ====================
    private String title;
    private String content;

    // ==================== 멀티미디어 및 메타데이터 ====================
    @Builder.Default
    private List<String> hashtags = new ArrayList<>();

    @Builder.Default
    private List<String> images = new ArrayList<>();

    // ==================== 상태 관리 ====================
    private ContentStatus status;

    // ==================== 생성 조건 ====================
    private CreationConditions creationConditions;

    // ==================== 매장 정보 ====================
    private Long storeId;

    // ==================== 프로모션 기간 ====================
    private LocalDateTime promotionStartDate;
    private LocalDateTime promotionEndDate;

    // ==================== 메타데이터 ====================
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public Content(ContentId of, ContentType contentType, Platform platform, String title, String content, List<String> strings, List<String> strings1, ContentStatus contentStatus, CreationConditions conditions, Long storeId, LocalDateTime createdAt, LocalDateTime updatedAt) {
    }

    // ==================== 비즈니스 메서드 ====================

    /**
     * 콘텐츠 제목 수정
     * @param newTitle 새로운 제목
     */
    public void updateTitle(String newTitle) {
        if (newTitle == null || newTitle.trim().isEmpty()) {
            throw new IllegalArgumentException("제목은 필수입니다.");
        }
        this.title = newTitle.trim();
        this.updatedAt = LocalDateTime.now();
    }

    /**
     * 콘텐츠 내용 수정
     * @param newContent 새로운 내용
     */
    public void updateContent(String newContent) {
        this.content = newContent;
        this.updatedAt = LocalDateTime.now();
    }

    /**
     * 프로모션 기간 설정
     * @param startDate 시작일
     * @param endDate 종료일
     */
    public void updatePeriod(LocalDateTime startDate, LocalDateTime endDate) {
        if (startDate != null && endDate != null && startDate.isAfter(endDate)) {
            throw new IllegalArgumentException("시작일은 종료일보다 이후일 수 없습니다.");
        }
        this.promotionStartDate = startDate;
        this.promotionEndDate = endDate;
        this.updatedAt = LocalDateTime.now();
    }

    /**
     * 콘텐츠 상태 변경
     * @param newStatus 새로운 상태
     */
    public void updateStatus(ContentStatus newStatus) {
        if (newStatus == null) {
            throw new IllegalArgumentException("상태는 필수입니다.");
        }
        this.status = newStatus;
        this.updatedAt = LocalDateTime.now();
    }

    /**
     * 해시태그 추가
     * @param hashtag 추가할 해시태그
     */
    public void addHashtag(String hashtag) {
        if (hashtag != null && !hashtag.trim().isEmpty()) {
            if (this.hashtags == null) {
                this.hashtags = new ArrayList<>();
            }
            this.hashtags.add(hashtag.trim());
            this.updatedAt = LocalDateTime.now();
        }
    }

    /**
     * 이미지 추가
     * @param imageUrl 추가할 이미지 URL
     */
    public void addImage(String imageUrl) {
        if (imageUrl != null && !imageUrl.trim().isEmpty()) {
            if (this.images == null) {
                this.images = new ArrayList<>();
            }
            this.images.add(imageUrl.trim());
            this.updatedAt = LocalDateTime.now();
        }
    }

    /**
     * 프로모션 진행 중 여부 확인
     * @return 현재 시간이 프로모션 기간 내에 있으면 true
     */
    public boolean isPromotionActive() {
        if (promotionStartDate == null || promotionEndDate == null) {
            return false;
        }
        LocalDateTime now = LocalDateTime.now();
        return !now.isBefore(promotionStartDate) && !now.isAfter(promotionEndDate);
    }

    /**
     * 콘텐츠 게시 가능 여부 확인
     * @return 필수 정보가 모두 입력되어 있으면 true
     */
    public boolean canBePublished() {
        return title != null && !title.trim().isEmpty()
                && contentType != null
                && platform != null
                && storeId != null;
    }
}