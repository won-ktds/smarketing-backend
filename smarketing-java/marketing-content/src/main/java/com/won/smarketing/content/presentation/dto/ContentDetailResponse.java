package com.won.smarketing.content.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 콘텐츠 상세 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "콘텐츠 상세 응답")
public class ContentDetailResponse {

    @Schema(description = "콘텐츠 ID", example = "1")
    private Long contentId;

    @Schema(description = "콘텐츠 타입", example = "SNS_POST")
    private String contentType;

    @Schema(description = "플랫폼", example = "INSTAGRAM")
    private String platform;

    @Schema(description = "제목", example = "맛있는 신메뉴를 소개합니다!")
    private String title;

    @Schema(description = "콘텐츠 내용")
    private String content;

    @Schema(description = "해시태그 목록")
    private List<String> hashtags;

    @Schema(description = "이미지 URL 목록")
    private List<String> images;

    @Schema(description = "상태", example = "PUBLISHED")
    private String status;

    @Schema(description = "홍보 시작일")
    private LocalDateTime promotionStartDate;

    @Schema(description = "홍보 종료일")
    private LocalDateTime promotionEndDate;

    @Schema(description = "생성 조건")
    private CreationConditionsDto creationConditions;

    @Schema(description = "생성일시")
    private LocalDateTime createdAt;

    @Schema(description = "수정일시")
    private LocalDateTime updatedAt;

    /**
     * 생성 조건 내부 DTO
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "콘텐츠 생성 조건")
    public static class CreationConditionsDto {

        @Schema(description = "톤앤매너", example = "친근함")
        private String toneAndManner;

        @Schema(description = "프로모션 유형", example = "할인 정보")
        private String promotionType;

        @Schema(description = "감정 강도", example = "보통")
        private String emotionIntensity;

        @Schema(description = "홍보 대상", example = "메뉴")
        private String targetAudience;

        @Schema(description = "이벤트명", example = "신메뉴 출시 이벤트")
        private String eventName;
    }
}