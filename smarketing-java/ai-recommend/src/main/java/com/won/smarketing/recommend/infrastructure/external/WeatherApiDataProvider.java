package com.won.smarketing.recommend.infrastructure.external;

import com.won.smarketing.common.exception.BusinessException;
import com.won.smarketing.common.exception.ErrorCode;
import com.won.smarketing.recommend.domain.model.WeatherData;
import com.won.smarketing.recommend.domain.service.WeatherDataProvider;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import reactor.core.publisher.Mono;

import java.time.Duration;

/**
 * 날씨 API 데이터 제공자 구현체
 * 외부 날씨 API를 통해 날씨 정보 조회
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class WeatherApiDataProvider implements WeatherDataProvider {

    private final WebClient webClient;

    @Value("${external.weather-api.api-key}")
    private String weatherApiKey;

    @Value("${external.weather-api.base-url}")
    private String weatherApiBaseUrl;

    /**
     * 특정 위치의 현재 날씨 정보 조회
     * 
     * @param location 위치 (주소)
     * @return 날씨 데이터
     */
    @Override
    public WeatherApiResponse getCurrentWeather(String location) {
        try {
            log.debug("날씨 정보 조회 시작: location={}", location);
            
            // 한국 주요 도시로 단순화
            String city = extractCity(location);
            
            WeatherApiResponse response = webClient
                    .get()
                    .uri(uriBuilder -> uriBuilder
                            .scheme("https")
                            .host("api.openweathermap.org")
                            .path("/data/2.5/weather")
                            .queryParam("q", city + ",KR")
                            .queryParam("appid", weatherApiKey)
                            .queryParam("units", "metric")
                            .queryParam("lang", "kr")
                            .build())
                    .retrieve()
                    .bodyToMono(WeatherApiResponse.class)
                    .timeout(Duration.ofSeconds(10))
                    .onErrorReturn(createDefaultWeatherData()) // 오류 시 기본값 반환
                    .block();

            if (response == null) {
                return createDefaultWeatherData();
            }

            WeatherData weatherData = WeatherData.builder()
                    .temperature(response.getMain().getTemp())
                    .condition(response.getWeather()[0].getDescription())
                    .humidity(response.getMain().getHumidity())
                    .build();

            log.debug("날씨 정보 조회 완료: {}도, {}", weatherData.getTemperature(), weatherData.getCondition());
            return weatherData;

        } catch (Exception e) {
            log.warn("날씨 정보 조회 실패, 기본값 사용: location={}", location, e);
            return createDefaultWeatherData();
        }
    }

    /**
     * 주소에서 도시명 추출
     * 
     * @param location 전체 주소
     * @return 도시명
     */
    private String extractCity(String location) {
        if (location == null || location.trim().isEmpty()) {
            return "Seoul";
        }
        
        // 서울, 부산, 대구, 인천, 광주, 대전, 울산 등 주요 도시 추출
        String[] cities = {"서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종", "수원", "창원"};
        
        for (String city : cities) {
            if (location.contains(city)) {
                return city;
            }
        }
        
        return "Seoul"; // 기본값
    }

    /**
     * 기본 날씨 데이터 생성 (API 호출 실패 시 사용)
     * 
     * @return 기본 날씨 데이터
     */
    private WeatherApiResponse createDefaultWeatherData() {
        WeatherApiResponse response = new WeatherApiResponse();
        response.setMain(new WeatherApiResponse.Main());
        response.getMain().setTemp(20.0); // 기본 온도 20도
        response.getMain().setHumidity(60.0); // 기본 습도 60%
        
        WeatherApiResponse.Weather[] weather = new WeatherApiResponse.Weather[1];
        weather[0] = new WeatherApiResponse.Weather();
        weather[0].setDescription("맑음");
        response.setWeather(weather);
        
        return response;
    }

    /**
     * 날씨 API 응답 DTO
     */
    private static class WeatherApiResponse {
        private Main main;
        private Weather[] weather;

        public Main getMain() { return main; }
        public void setMain(Main main) { this.main = main; }
        public Weather[] getWeather() { return weather; }
        public void setWeather(Weather[] weather) { this.weather = weather; }

        static class Main {
            private Double temp;
            private Double humidity;

            public Double getTemp() { return temp; }
            public void setTemp(Double temp) { this.temp = temp; }
            public Double getHumidity() { return humidity; }
            public void setHumidity(Double humidity) { this.humidity = humidity; }
        }

        static class Weather {
            private String description;

            public String getDescription() { return description; }
            public void setDescription(String description) { this.description = description; }
        }
    }
}
