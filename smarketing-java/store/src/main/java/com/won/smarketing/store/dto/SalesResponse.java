package com.won.smarketing.store.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

/**
 * 매출 응답 DTO
 * 매출 정보를 클라이언트에게 전달합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "매출 응답")
public class SalesResponse {
    
    @Schema(description = "오늘 매출", example = "150000")
    private BigDecimal todaySales;
    
    @Schema(description = "월간 매출", example = "4500000")
    private BigDecimal monthSales;
    
    @Schema(description = "전일 대비 매출 변화", example = "25000")
    private BigDecimal previousDayComparison;
    
    @Schema(description = "전일 대비 매출 변화율 (%)", example = "15.5")
    private BigDecimal previousDayChangeRate;
    
    @Schema(description = "목표 매출 대비 달성율 (%)", example = "85.2")
    private BigDecimal goalAchievementRate;
}
