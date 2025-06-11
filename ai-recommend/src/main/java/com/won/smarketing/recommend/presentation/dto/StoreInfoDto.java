package com.won.smarketing.recommend.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 매장 정보 DTO
 * AI 마케팅 팁 생성 시 매장 특성을 반영하기 위한 정보입니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "매장 정보")
public class StoreInfoDto {
    
    @Schema(description = "매장명", example = "카페 원더풀")
    private String storeName;
    
    @Schema(description = "업종", example = "카페")
    private String businessType;
    
    @Schema(description = "매장 위치", example = "서울시 강남구")
    private String location;
}
