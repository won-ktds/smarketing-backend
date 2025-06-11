package com.won.smarketing.recommend.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 날씨 정보 DTO
 * AI 마케팅 팁 생성 시 참고되는 환경 데이터입니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "날씨 정보")
public class WeatherInfoDto {
    
    @Schema(description = "기온 (섭씨)", example = "23.5")
    private Double temperature;
    
    @Schema(description = "날씨 상태", example = "맑음")
    private String condition;
    
    @Schema(description = "습도 (%)", example = "65.0")
    private Double humidity;
}
