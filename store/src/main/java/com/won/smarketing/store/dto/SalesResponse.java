package com.won.smarketing.store.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

/**
 * 매출 정보 응답 DTO
 * 오늘 매출, 월간 매출, 전일 대비 매출 정보
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "매출 정보 응답")
public class SalesResponse {

    @Schema(description = "오늘 매출", example = "150000")
    private BigDecimal todaySales;

    @Schema(description = "이번 달 매출", example = "3200000")
    private BigDecimal monthSales;

    @Schema(description = "전일 대비 매출 변화량", example = "25000")
    private BigDecimal previousDayComparison;
}
