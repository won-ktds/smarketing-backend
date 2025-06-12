package com.won.smarketing.recommend.application.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

/**
 * 날씨 데이터 서비스 (Mock)
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class WeatherDataService {

    @Cacheable(value = "weatherData", key = "#location")
    public com.won.smarketing.recommend.service.MarketingTipService.WeatherInfo getCurrentWeather(String location) {
        log.debug("날씨 정보 조회: location={}", location);

        // Mock 데이터 반환
        double temperature = 20.0 + (Math.random() * 15); // 20-35도
        String[] conditions = {"맑음", "흐림", "비", "눈", "안개"};
        String condition = conditions[(int) (Math.random() * conditions.length)];
        double humidity = 50.0 + (Math.random() * 30); // 50-80%

        return com.won.smarketing.recommend.service.MarketingTipService.WeatherInfo.builder()
                .temperature(Math.round(temperature * 10) / 10.0)
                .condition(condition)
                .humidity(Math.round(humidity * 10) / 10.0)
                .build();
    }
}