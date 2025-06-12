package com.won.smarketing.recommend.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

@Schema(description = "마케팅 팁 생성 요청")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MarketingTipRequest {

    @Schema(description = "매장 ID", example = "1", required = true)
    @NotNull(message = "매장 ID는 필수입니다")
    @Positive(message = "매장 ID는 양수여야 합니다")
    private Long storeId;

    @Schema(description = "추가 요청사항", example = "여름철 음료 프로모션에 집중해주세요")
    private String additionalRequirement;
}
