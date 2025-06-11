package com.won.smarketing.content.domain.model;

import lombok.*;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

/**
 * 마케팅 콘텐츠 도메인 모델
 * 콘텐츠의 핵심 비즈니스 로직과 상태를 관리
 */
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
@Builder
public class Content {

    /**
     * 콘텐츠 고유 식별자
     */
    private ContentId id;

    /**
     * 콘텐츠 타입 (SNS 게시물, 포스터 등)
     */
    private ContentType contentType;

    /**
     * 플랫폼 (인스타그램, 네이버 블로그 등)
     */
    private Platform platform;

    /**
     * 콘텐츠 제목
     */
    private String title;

    /**
     * 콘텐츠 내용
     */
    private String content;

    /**
     * 해시태그 목록
     */
    private List<String> hashtags;

    /**
     * 이미지 URL 목록
     */
    private List<String> images;

    /**
     * 콘텐츠 상태
     */
    private ContentStatus status;

    /**
     * 콘텐츠 생성 조건
     */
    private CreationConditions creationConditions;

    /**
     * 매장 ID
     */
    private Long storeId;

    /**
     * 생성 시각
     */
    private LocalDateTime createdAt;

    /**
     * 수정 시각
     */
    private LocalDateTime updatedAt;

    /**
     * 콘텐츠 제목 업데이트
     * 
     * @param title 새로운 제목
     */
    public void updateTitle(String title) {
        this.title = title;
        this.updatedAt = LocalDateTime.now();
    }

    /**
     * 콘텐츠 기간 업데이트
     * 
     * @param startDate 시작일
     * @param endDate 종료일
     */
    public void updatePeriod(LocalDate startDate, LocalDate endDate) {
        if (this.creationConditions != null) {
            this.creationConditions = this.creationConditions.toBuilder()
                    .startDate(startDate)
                    .endDate(endDate)
                    .build();
        }
        this.updatedAt = LocalDateTime.now();
    }

    /**
     * 콘텐츠 상태 변경
     * 
     * @param status 새로운 상태
     */
    public void changeStatus(ContentStatus status) {
        this.status = status;
        this.updatedAt = LocalDateTime.now();
    }
}
