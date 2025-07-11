package com.won.smarketing.recommend.domain.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.cglib.core.Local;

import java.time.LocalDateTime;

/**
 * 마케팅 팁 도메인 모델 (날씨 정보 제거)
 */
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MarketingTip {

    private TipId id;
    private Long storeId;
    private String tipSummary;
    private String tipContent;
    private StoreWithMenuData storeWithMenuData;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public static MarketingTip create(Long storeId, String tipContent, StoreWithMenuData storeWithMenuData) {
        return MarketingTip.builder()
                .storeId(storeId)
                .tipContent(tipContent)
                .storeWithMenuData(storeWithMenuData)
                .createdAt(LocalDateTime.now())
                .build();
    }
}