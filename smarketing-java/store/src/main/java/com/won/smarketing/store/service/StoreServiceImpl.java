package com.won.smarketing.store.service;

import com.won.smarketing.common.exception.BusinessException;
import com.won.smarketing.common.exception.ErrorCode;
import com.won.smarketing.store.dto.StoreCreateRequest;
import com.won.smarketing.store.dto.StoreCreateResponse;
import com.won.smarketing.store.dto.StoreResponse;
import com.won.smarketing.store.dto.StoreUpdateRequest;
import com.won.smarketing.store.entity.Store;
import com.won.smarketing.store.repository.StoreRepository;
import jakarta.xml.bind.annotation.XmlType;
import lombok.Builder;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 매장 서비스 구현체
 * 매장 등록, 조회, 수정 기능 구현
 */
@Slf4j
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class StoreServiceImpl implements StoreService {

    private final StoreRepository storeRepository;

    /**
     * 매장 등록
     * 
     * @param request 매장 등록 요청 정보
     * @return 등록된 매장 정보
     */
    @Override
    @Transactional
    public StoreCreateResponse register(StoreCreateRequest request) {
        String memberId = getCurrentUserId();
      //  Long memberId = Long.valueOf(currentUserId); // 실제로는 Member ID 조회 필요
        
        log.info("매장 등록 시작: {} (회원: {})", request.getStoreName(), memberId);
        
        // 회원당 하나의 매장만 등록 가능
        if (storeRepository.existsByUserId(memberId)) {
            throw new BusinessException(ErrorCode.STORE_ALREADY_EXISTS);
        }
        
        // 매장 엔티티 생성 및 저장
        Store store = Store.builder()
                .userId(memberId)
                .storeName(request.getStoreName())
                .businessType(request.getBusinessType())
                .address(request.getAddress())
                .phoneNumber(request.getPhoneNumber())
                .businessHours(request.getBusinessHours())
                .closedDays(request.getClosedDays())
                .seatCount(request.getSeatCount())
                .blogAccounts(request.getBlogAccounts())
                .instaAccounts(request.getInstaAccounts())
                .description(request.getDescription())
                .build();
        
        Store savedStore = storeRepository.save(store);
        log.info("매장 등록 완료: {} (ID: {})", savedStore.getStoreName(), savedStore.getId());
        
        return toStoreCreateResponse(savedStore);
    }

    /**
     * 매장 정보 조회 (현재 로그인 사용자)
     * 
     * @return 매장 정보
     */
    @Override
    public StoreResponse getMyStore() {
        String memberId = getCurrentUserId();
       // Long memberId = Long.valueOf(currentUserId);
        
        Store store = storeRepository.findByUserId(memberId)
                .orElseThrow(() -> new BusinessException(ErrorCode.STORE_NOT_FOUND));
        
        return toStoreResponse(store);
    }

    /**
     * 매장 정보 조회 (매장 ID)
     * 
     * //@param storeId 매장 ID
     * @return 매장 정보
     */
    @Override
    public StoreResponse getStore() {
        try {
            String userId = getCurrentUserId();
            Store store = storeRepository.findByUserId(userId)
                    .orElseThrow(() -> new BusinessException(ErrorCode.STORE_NOT_FOUND));
            
            return toStoreResponse(store);
        } catch (NumberFormatException e) {
            throw new BusinessException(ErrorCode.INVALID_INPUT_VALUE);
        }
    }

    /**
     * 매장 정보 수정
     * 
     * //@param storeId 매장 ID
     * @param request 매장 수정 요청 정보
     * @return 수정된 매장 정보
     */
    @Override
    @Transactional
    public StoreResponse updateStore(StoreUpdateRequest request) {
        String userId = getCurrentUserId();

        Store store = storeRepository.findByUserId(userId)
                .orElseThrow(() -> new BusinessException(ErrorCode.STORE_NOT_FOUND));
        
        // 매장 정보 업데이트
        store.updateStore(
                request.getStoreName(),
                request.getBusinessType(),
                request.getAddress(),
                request.getPhoneNumber(),
                request.getBusinessHours(),
                request.getClosedDays(),
                request.getSeatCount(),
                request.getInstaAccounts(),
                request.getBlogAccounts(),
                request.getDescription()
        );
        
        Store updatedStore = storeRepository.save(store);
        log.info("매장 정보 수정 완료: {} (ID: {})", updatedStore.getStoreName(), updatedStore.getId());
        
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
                .businessType(store.getBusinessType())
                .address(store.getAddress())
                .phoneNumber(store.getPhoneNumber())
                .businessHours(store.getBusinessHours())
                .closedDays(store.getClosedDays())
                .seatCount(store.getSeatCount())
                .blogAccounts(store.getBlogAccounts())
                .instaAccounts(store.getInstaAccounts())
                .description(store.getDescription())
                .createdAt(store.getCreatedAt())
                .updatedAt(store.getUpdatedAt())
                .build();
    }

    private StoreCreateResponse toStoreCreateResponse(Store store) {
        return StoreCreateResponse.builder()
                .storeId(store.getId())
//                .storeName(store.getStoreName())
//                .businessType(store.getBusinessType())
//                .address(store.getAddress())
//                .phoneNumber(store.getPhoneNumber())
//                .businessHours(store.getBusinessHours())
//                .closedDays(store.getClosedDays())
//                .seatCount(store.getSeatCount())
//                .snsAccounts(store.getSnsAccounts())
//                .description(store.getDescription())
//                .createdAt(store.getCreatedAt())
//                .updatedAt(store.getUpdatedAt())
                .build();
    }

    /**
     * 현재 로그인된 사용자 ID 조회
     * 
     * @return 사용자 ID
     */
    private String getCurrentUserId() {
        return SecurityContextHolder.getContext().getAuthentication().getName();
    }
}
