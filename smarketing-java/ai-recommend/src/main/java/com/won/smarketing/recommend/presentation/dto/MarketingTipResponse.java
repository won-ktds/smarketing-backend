package com.won.smarketing.recommend.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Schema(description = "마케팅 팁 응답")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MarketingTipResponse {

    @Schema(description = "팁 ID", example = "1")
    private Long tipId;

    @Schema(description = "매장 ID", example = "1")
    private Long storeId;

    @Schema(description = "매장명", example = "카페 봄날")
    private String storeName;

    @Schema(description = "AI 생성 마케팅 팁 내용")
    private String tipContent;

    @Schema(description = "날씨 정보")
    private WeatherInfo weatherInfo;

    @Schema(description = "매장 정보")
    private StoreInfo storeInfo;

    @Schema(description = "생성 일시")
    private LocalDateTime createdAt;

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class WeatherInfo {
        @Schema(description = "온도", example = "25.5")
        private Double temperature;

        @Schema(description = "날씨 상태", example = "맑음")
        private String condition;

        @Schema(description = "습도", example = "60.0")
        private Double humidity;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class StoreInfo {
        @Schema(description = "매장명", example = "카페 봄날")
        private String storeName;

        @Schema(description = "업종", example = "카페")
        private String businessType;

        @Schema(description = "위치", example = "서울시 강남구")
        private String location;
    }
}