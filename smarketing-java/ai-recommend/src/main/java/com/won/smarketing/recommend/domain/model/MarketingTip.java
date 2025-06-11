package com.won.smarketing.recommend.domain.model;

import com.won.smarketing.recommend.domain.model.StoreData;
import com.won.smarketing.recommend.domain.model.TipId;
import com.won.smarketing.recommend.domain.model.WeatherData;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 마케팅 팁 도메인 모델
 */
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MarketingTip {

    private TipId id;
    private Long storeId;
    private String tipContent;
    private WeatherData weatherData;
    private StoreData storeData;
    private LocalDateTime createdAt;

    public static MarketingTip create(Long storeId, String tipContent, WeatherData weatherData, StoreData storeData) {
        return MarketingTip.builder()
                .storeId(storeId)
                .tipContent(tipContent)
                .weatherData(weatherData)
                .storeData(storeData)
                .createdAt(LocalDateTime.now())
                .build();
    }
}