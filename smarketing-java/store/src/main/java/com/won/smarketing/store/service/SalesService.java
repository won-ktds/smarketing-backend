package com.won.smarketing.store.service;

import com.won.smarketing.store.dto.SalesResponse;

/**
 * 매출 서비스 인터페이스
 * 매출 조회 관련 비즈니스 로직 정의
 */
public interface SalesService {
    
    /**
     * 매출 정보 조회
     * 
     * @return 매출 정보
     */
    SalesResponse getSales(Long storeId);
}
