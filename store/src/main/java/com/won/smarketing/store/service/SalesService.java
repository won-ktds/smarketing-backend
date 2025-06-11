package com.won.smarketing.store.service;

import com.won.smarketing.store.dto.SalesResponse;

/**
 * 매출 관리 서비스 인터페이스
 * 매출 조회 기능 정의
 */
public interface SalesService {
    
    /**
     * 매출 정보 조회
     * 
     * @return 매출 정보 (오늘, 월간, 전일 대비)
     */
    SalesResponse getSales();
}
