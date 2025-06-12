package com.won.smarketing.recommend.domain.service;

import com.won.smarketing.recommend.domain.model.StoreData;

/**
 * AI 팁 생성 도메인 서비스 인터페이스 (단순화)
 */
public interface AiTipGenerator {
    
    /**
     * Python AI 서비스를 통한 마케팅 팁 생성
     * 
     * @param storeData 매장 정보
     * @param additionalRequirement 추가 요청사항
     * @return AI가 생성한 마케팅 팁
     */
    String generateTip(StoreData storeData, String additionalRequirement);
}
