package com.won.smarketing.store.service;

import com.won.smarketing.common.exception.BusinessException;
import com.won.smarketing.common.exception.ErrorCode;
import com.won.smarketing.store.dto.StoreCreateRequest;
import com.won.smarketing.store.dto.StoreResponse;
import com.won.smarketing.store.dto.StoreUpdateRequest;
import com.won.smarketing.store.entity.Store;
import com.won.smarketing.store.repository.StoreRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 매장 관리 서비스 구현체
 * 매장 등록, 조회, 수정 기능 구현
 */
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class StoreServiceImpl implements StoreService {

    private final StoreRepository storeRepository;

    /**
     * 매장 정보 등록
     * 
     * @param request 매장 등록 요청 정보
     * @return 등록된 매장 정보
     */
    @Override
    @Transactional
    public StoreResponse register(StoreCreateRequest request) {
        // 사용자별 매장 중복 등록 확인
        if (storeRepository.findByUserId(request.getUserId()).isPresent()) {
            throw new BusinessException(ErrorCode.STORE_ALREADY_EXISTS);
        }

        // 매장 엔티티 생성 및 저장
        Store store = Store.builder()
                .userId(request.getUserId())
                .storeName(request.getStoreName())
                .storeImage(request.getStoreImage())
                .businessType(request.getBusinessType())
                .address(request.getAddress())
                .phoneNumber(request.getPhoneNumber())
                .businessNumber(request.getBusinessNumber())
                .instaAccount(request.getInstaAccount())
                .naverBlogAccount(request.getNaverBlogAccount())
                .openTime(request.getOpenTime())
                .closeTime(request.getCloseTime())
                .closedDays(request.getClosedDays())
                .seatCount(request.getSeatCount())
                .build();

        Store savedStore = storeRepository.save(store);
        return toStoreResponse(savedStore);
    }

    /**
     * 매장 정보 조회
     * 
     * @param storeId 조회할 매장 ID
     * @return 매장 정보
     */
    @Override
    public StoreResponse getStore(String storeId) {
        Store store = storeRepository.findByUserId(storeId)
                .orElseThrow(() -> new BusinessException(ErrorCode.STORE_NOT_FOUND));
        
        return toStoreResponse(store);
    }

    /**
     * 매장 정보 수정
     * 
     * @param storeId 수정할 매장 ID
     * @param request 매장 수정 요청 정보
     * @return 수정된 매장 정보
     */
    @Override
    @Transactional
    public StoreResponse updateStore(Long storeId, StoreUpdateRequest request) {
        Store store = storeRepository.findById(storeId)
                .orElseThrow(() -> new BusinessException(ErrorCode.STORE_NOT_FOUND));

        // 매장 정보 업데이트
        store.updateStoreInfo(
                request.getStoreName(),
                request.getStoreImage(),
                request.getAddress(),
                request.getPhoneNumber(),
                request.getInstaAccount(),
                request.getNaverBlogAccount(),
                request.getOpenTime(),
                request.getCloseTime(),
                request.getClosedDays(),
                request.getSeatCount()
        );

        Store updatedStore = storeRepository.save(store);
        return toStoreResponse(updatedStore);
    }

    /**
     * Store 엔티티를 StoreResponse DTO로 변환
     * 
     * @param store Store 엔티티
     * @return StoreResponse DTO
     */
    private StoreResponse toStoreResponse(Store store) {
        return StoreResponse.builder()
                .storeId(store.getId())
                .storeName(store.getStoreName())
                .storeImage(store.getStoreImage())
                .businessType(store.getBusinessType())
                .address(store.getAddress())
                .phoneNumber(store.getPhoneNumber())
                .businessNumber(store.getBusinessNumber())
                .instaAccount(store.getInstaAccount())
                .naverBlogAccount(store.getNaverBlogAccount())
                .openTime(store.getOpenTime())
                .closeTime(store.getCloseTime())
                .closedDays(store.getClosedDays())
                .seatCount(store.getSeatCount())
                .createdAt(store.getCreatedAt())
                .updatedAt(store.getUpdatedAt())
                .build();
    }
}
