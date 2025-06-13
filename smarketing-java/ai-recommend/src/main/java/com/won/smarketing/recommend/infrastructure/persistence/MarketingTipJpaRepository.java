package com.won.smarketing.recommend.infrastructure.persistence;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

/**
 * 마케팅 팁 JPA 레포지토리
 */
@Repository
public interface MarketingTipJpaRepository extends JpaRepository<MarketingTipEntity, Long> {
    
    @Query("SELECT m FROM MarketingTipEntity m WHERE m.storeId = :storeId ORDER BY m.createdAt DESC")
    Page<MarketingTipEntity> findByStoreIdOrderByCreatedAtDesc(@Param("storeId") Long storeId, Pageable pageable);
}
