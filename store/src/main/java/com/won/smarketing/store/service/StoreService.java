package com.won.smarketing.store.service;

import com.won.smarketing.store.dto.StoreCreateRequest;
import com.won.smarketing.store.dto.StoreResponse;
import com.won.smarketing.store.dto.StoreUpdateRequest;

/**
 * 매장 관리 서비스 인터페이스
 * 매장 등록, 조회, 수정 기능 정의
 */
public interface StoreService {
    
    /**
     * 매장 정보 등록
     * 
     * @param request 매장 등록 요청 정보
     * @return 등록된 매장 정보
     */
    StoreResponse register(StoreCreateRequest request);
    
    /**
     * 매장 정보 조회
     * 
     * @param storeId 조회할 매장 ID
     * @return 매장 정보
     */
    StoreResponse getStore(String storeId);
    
    /**
     * 매장 정보 수정
     * 
     * @param storeId 수정할 매장 ID
     * @param request 매장 수정 요청 정보
     * @return 수정된 매장 정보
     */
    StoreResponse updateStore(Long storeId, StoreUpdateRequest request);
}
