package com.won.smarketing.recommend.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * AI 마케팅 팁 생성 응답 DTO
 * AI가 생성한 개인화된 마케팅 팁 정보를 전달합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "AI 마케팅 팁 생성 응답")
public class MarketingTipResponse {
    
    @Schema(description = "팁 ID", example = "1")
    private Long tipId;
    
    @Schema(description = "AI 생성 마케팅 팁 내용 (100자 이내)", 
            example = "오늘 같은 비 오는 날에는 따뜻한 음료와 함께 실내 분위기를 강조한 포스팅을 올려보세요. #비오는날카페 #따뜻한음료 해시태그로 감성을 어필해보세요!")
    private String tipContent;
    
    @Schema(description = "팁 생성 시간", example = "2024-01-15T10:30:00")
    private LocalDateTime createdAt;
}
