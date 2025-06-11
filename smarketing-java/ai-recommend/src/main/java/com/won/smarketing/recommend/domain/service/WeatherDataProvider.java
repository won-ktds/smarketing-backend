package com.won.smarketing.recommend.domain.service;

import com.won.smarketing.recommend.domain.model.WeatherData;

/**
 * 날씨 데이터 제공 도메인 서비스 인터페이스
 * 외부 날씨 API로부터 날씨 정보 조회 기능 정의
 */
public interface WeatherDataProvider {

    /**
     * 특정 위치의 현재 날씨 정보 조회
     *
     * @param location 위치 (주소)
     * @return 날씨 데이터
     */
    WeatherData getCurrentWeather(String location);
}