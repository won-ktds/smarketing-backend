package com.won.smarketing.recommend.domain.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * 날씨 데이터 값 객체
 */
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class WeatherData {
    private Double temperature;
    private String condition;
    private Double humidity;
}