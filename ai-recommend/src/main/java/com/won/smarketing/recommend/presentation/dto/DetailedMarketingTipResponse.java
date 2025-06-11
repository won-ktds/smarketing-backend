package com.won.smarketing.recommend.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 상세 AI 마케팅 팁 응답 DTO
 * AI 마케팅 팁과 함께 생성 시 사용된 환경 데이터도 포함합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "상세 AI 마케팅 팁 응답")
public class DetailedMarketingTipResponse {
    
    @Schema(description = "팁 ID", example = "1")
    private Long tipId;
    
    @Schema(description = "AI 생성 마케팅 팁 내용 (100자 이내)")
    private String tipContent;
    
    @Schema(description = "팁 생성 시간", example = "2024-01-15T10:30:00")
    private LocalDateTime createdAt;
    
    @Schema(description = "팁 생성 시 참고된 날씨 정보")
    private WeatherInfoDto weatherInfo;
    
    @Schema(description = "팁 생성 시 참고된 매장 정보")
    private StoreInfoDto storeInfo;
}
