package com.won.smarketing.content.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 진행 중인 콘텐츠 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "진행 중인 콘텐츠 응답")
public class OngoingContentResponse {

    @Schema(description = "콘텐츠 ID", example = "1")
    private Long contentId;

    @Schema(description = "콘텐츠 타입", example = "SNS_POST")
    private String contentType;

    @Schema(description = "플랫폼", example = "INSTAGRAM")
    private String platform;

    @Schema(description = "제목", example = "진행 중인 이벤트")
    private String title;

    @Schema(description = "상태", example = "PUBLISHED")
    private String status;

    @Schema(description = "홍보 시작일")
    private LocalDateTime promotionStartDate;

    @Schema(description = "홍보 종료일")
    private LocalDateTime promotionEndDate;

    @Schema(description = "남은 일수", example = "5")
    private Long remainingDays;

    @Schema(description = "진행률 (%)", example = "60.5")
    private Double progressPercentage;
}