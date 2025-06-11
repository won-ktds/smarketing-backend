package com.won.smarketing.recommend.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * AI 마케팅 팁 생성을 위한 내부 요청 DTO
 * 애플리케이션 계층에서 AI 서비스 호출 시 사용됩니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "AI 마케팅 팁 생성 내부 요청")
public class MarketingTipGenerationRequest {
    
    @NotNull(message = "매장 정보는 필수입니다")
    @Schema(description = "매장 정보", required = true)
    private StoreInfoDto storeInfo;
    
    @Schema(description = "현재 날씨 정보")
    private WeatherInfoDto weatherInfo;
    
    @Schema(description = "팁 생성 옵션", example = "일반")
    private String tipType;
}
