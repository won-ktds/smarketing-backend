package com.won.smarketing.recommend.domain.service;

import com.won.smarketing.recommend.domain.model.StoreData;
import com.won.smarketing.recommend.domain.model.WeatherData;

/**
 * AI 팁 생성 도메인 서비스 인터페이스
 * AI를 활용한 마케팅 팁 생성 기능 정의
 */
public interface AiTipGenerator {
    
    /**
     * 매장 정보와 날씨 정보를 바탕으로 마케팅 팁 생성
     * 
     * @param storeData 매장 데이터
     * @param weatherData 날씨 데이터
     * @return AI가 생성한 마케팅 팁
     */
    String generateTip(StoreData storeData, WeatherData weatherData);
}
