package com.won.smarketing.recommend.domain.service;

import com.won.smarketing.recommend.domain.model.StoreData;

/**
 * 매장 데이터 제공 도메인 서비스 인터페이스
 */
public interface StoreDataProvider {

    /**
     * 사용자 ID로 매장 정보 조회
     *
     * @param userId 사용자 ID
     * @return 매장 정보
     */
    StoreData getStoreDataByUserId(String userId);
}
