package com.won.smarketing.store.repository;

import com.won.smarketing.store.entity.Store;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * 매장 정보 데이터 접근을 위한 Repository
 * JPA를 사용한 매장 CRUD 작업 처리
 */
@Repository
public interface StoreRepository extends JpaRepository<Store, Long> {
    
    /**
     * 회원 ID로 매장 조회
     * 
     * @param userId 회원 ID
     * @return 매장 정보 (Optional)
     */
    Optional<Store> findByUserId(String userId);
    
    /**
     * 회원의 매장 존재 여부 확인
     * 
     * @param userId 회원 ID
     * @return 존재 여부
     */
    boolean existsByUserId(String userId);
    
    /**
     * 매장명으로 매장 조회
     * 
     * @param storeName 매장명
     * @return 매장 목록
     */
    Optional<Store> findByStoreName(String storeName);
}



