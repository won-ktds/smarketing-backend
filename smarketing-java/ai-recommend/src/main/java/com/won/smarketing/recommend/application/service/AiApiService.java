package com.won.smarketing.recommend.domain.service;

import com.won.smarketing.recommend.domain.model.StoreData;
import com.won.smarketing.recommend.domain.model.WeatherData;

/**
 * Python AI 서비스 인터페이스
 * AI 처리를 Python 서비스로 위임하는 도메인 서비스
 */
public interface AiApiService {

    /**
     * Python AI 서비스를 통한 마케팅 팁 생성
     *
     * @param storeData 매장 정보
     * @param weatherData 날씨 정보
     * @param additionalRequirement 추가 요청사항
     * @return AI가 생성한 마케팅 팁 (한 줄)
     */
    String generateMarketingTip(StoreData storeData, WeatherData weatherData, String additionalRequirement);
}