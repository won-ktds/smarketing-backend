package com.won.smarketing.recommend.infrastructure.persistence;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * 마케팅 팁 JPA 레포지토리
 */
@Repository
public interface MarketingTipJpaRepository extends JpaRepository<MarketingTipEntity, Long> {

    /**
     * 매장별 마케팅 팁 조회 (기존 - storeId 기반)
     */
    @Query("SELECT m FROM MarketingTipEntity m WHERE m.storeId = :storeId ORDER BY m.createdAt DESC")
    Page<MarketingTipEntity> findByStoreIdOrderByCreatedAtDesc(@Param("storeId") Long storeId, Pageable pageable);

    /**
     * 사용자별 마케팅 팁 조회 (새로 추가 - userId 기반)
     */
    @Query("SELECT m FROM MarketingTipEntity m WHERE m.userId = :userId ORDER BY m.createdAt DESC")
    Page<MarketingTipEntity> findByUserIdOrderByCreatedAtDesc(@Param("userId") String userId, Pageable pageable);

    /**
     * 사용자의 가장 최근 마케팅 팁 조회
     */
    @Query("SELECT m FROM MarketingTipEntity m WHERE m.userId = :userId ORDER BY m.createdAt DESC LIMIT 1")
    Optional<MarketingTipEntity> findTopByUserIdOrderByCreatedAtDesc(@Param("userId") String userId);

    /**
     * 특정 팁이 해당 사용자의 것인지 확인
     */
    boolean existsByIdAndUserId(Long id, String userId);
}