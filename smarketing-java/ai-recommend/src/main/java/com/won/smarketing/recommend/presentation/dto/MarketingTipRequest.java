package com.won.smarketing.recommend.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * AI 마케팅 팁 생성 요청 DTO
 * 매장 정보를 기반으로 개인화된 마케팅 팁을 요청할 때 사용됩니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "AI 마케팅 팁 생성 요청")
public class MarketingTipRequest {
    
    @NotNull(message = "매장 ID는 필수입니다")
    @Positive(message = "매장 ID는 양수여야 합니다")
    @Schema(description = "매장 ID", example = "1", required = true)
    private Long storeId;
}
