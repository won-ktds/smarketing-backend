package com.won.smarketing.recommend.domain.service;

import com.won.smarketing.recommend.domain.model.StoreWithMenuData;

import java.util.List;

/**
 * 매장 데이터 제공 도메인 서비스 인터페이스
 */
public interface StoreDataProvider {

    StoreWithMenuData getStoreWithMenuData(String userId);
}
