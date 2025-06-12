package com.won.smarketing.recommend.infrastructure.external;

import com.won.smarketing.recommend.domain.model.WeatherData;
import com.won.smarketing.recommend.domain.service.WeatherDataProvider;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.Duration;

/**
 * 날씨 API 데이터 제공자 구현체
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class WeatherApiDataProvider implements WeatherDataProvider {

    private final WebClient webClient;

    @Value("${external.weather-api.api-key}")
    private String weatherApiKey;

    @Value("${external.weather-api.timeout}")
    private int timeout;

    @Override
    @Cacheable(value = "weatherData", key = "#location")
    public WeatherData getCurrentWeather(String location) {
        try {
            log.debug("날씨 정보 조회: location={}", location);

            // 개발 환경에서는 Mock 데이터 반환
            if (weatherApiKey.equals("dummy-key")) {
                return createMockWeatherData(location);
            }

            // 실제 날씨 API 호출 (향후 구현)
            return callWeatherApi(location);

        } catch (Exception e) {
            log.warn("날씨 정보 조회 실패, Mock 데이터 사용: location={}", location, e);
            return createMockWeatherData(location);
        }
    }

    private WeatherData callWeatherApi(String location) {
        // 실제 OpenWeatherMap API 호출 로직 (향후 구현)
        log.info("실제 날씨 API 호출: {}", location);
        return createMockWeatherData(location);
    }

    private WeatherData createMockWeatherData(String location) {
        double temperature = 20.0 + (Math.random() * 15); // 20-35도
        String[] conditions = {"맑음", "흐림", "비", "눈", "안개"};
        String condition = conditions[(int) (Math.random() * conditions.length)];
        double humidity = 50.0 + (Math.random() * 30); // 50-80%

        return WeatherData.builder()
                .temperature(Math.round(temperature * 10) / 10.0)
                .condition(condition)
                .humidity(Math.round(humidity * 10) / 10.0)
                .build();
    }
}