package com.won.smarketing.recommend.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 마케팅 팁 응답 DTO (요약 + 상세 통합)
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "마케팅 팁 응답")
public class MarketingTipResponse {

    @Schema(description = "팁 ID", example = "1")
    private Long tipId;

    @Schema(description = "마케팅 팁 요약 (1줄)", example = "가을 시즌 특별 음료로 고객들의 관심을 끌어보세요!")
    private String tipSummary;

    @Schema(description = "마케팅 팁 전체 내용", example = "가을이 다가오면서 고객들은 따뜻하고 계절감 있는 음료를 찾게 됩니다...")
    private String tipContent;

    @Schema(description = "매장 정보")
    private StoreInfo storeInfo;

    @Schema(description = "생성 시간", example = "2025-06-13T14:30:00")
    private LocalDateTime createdAt;

    @Schema(description = "수정 시간", example = "2025-06-13T14:30:00")
    private LocalDateTime updatedAt;

    @Schema(description = "1시간 이내 생성 여부", example = "true")
    private boolean isRecentlyCreated;

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "매장 정보")
    public static class StoreInfo {
        @Schema(description = "매장명", example = "민코의 카페")
        private String storeName;

        @Schema(description = "업종", example = "카페")
        private String businessType;

        @Schema(description = "위치", example = "서울시 강남구 테헤란로 123")
        private String location;
    }
}