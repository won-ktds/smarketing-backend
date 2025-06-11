package com.won.smarketing.recommend.domain.service;

import com.won.smarketing.recommend.domain.model.StoreData;

/**
 * 매장 데이터 제공 도메인 서비스 인터페이스
 * 외부 매장 서비스로부터 매장 정보 조회 기능 정의
 */
public interface StoreDataProvider {

    /**
     * 매장 정보 조회
     *
     * @param storeId 매장 ID
     * @return 매장 데이터
     */
    StoreData getStoreData(Long storeId);
}