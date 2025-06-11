package com.won.smarketing.recommend.presentation.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Map;

/**
 * Python AI 서비스 요청 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AIServiceRequest {

    private String serviceType;  // "marketing_tips", "business_insights", "trend_analysis"
    private Long storeId;
    private String category;
    private Map<String, Object> parameters;
    private Map<String, Object> context;  // 매장 정보, 과거 데이터 등
}