package com.won.smarketing.content.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Map;

/**
 * 콘텐츠 통계 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "콘텐츠 통계 응답")
public class ContentStatisticsResponse {

    @Schema(description = "총 콘텐츠 수", example = "150")
    private Long totalContents;

    @Schema(description = "이번 달 생성된 콘텐츠 수", example = "25")
    private Long thisMonthContents;

    @Schema(description = "발행된 콘텐츠 수", example = "120")
    private Long publishedContents;

    @Schema(description = "임시저장된 콘텐츠 수", example = "30")
    private Long draftContents;

    @Schema(description = "콘텐츠 타입별 통계")
    private Map<String, Long> contentTypeStats;

    @Schema(description = "플랫폼별 통계")
    private Map<String, Long> platformStats;

    @Schema(description = "월별 생성 통계 (최근 6개월)")
    private Map<String, Long> monthlyStats;
}