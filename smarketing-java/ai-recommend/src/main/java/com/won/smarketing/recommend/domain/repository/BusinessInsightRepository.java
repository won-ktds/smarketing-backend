package com.won.smarketing.recommend.domain.repository;

import com.won.smarketing.recommend.domain.model.BusinessInsight;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface BusinessInsightRepository extends JpaRepository<BusinessInsight, Long> {

    List<BusinessInsight> findByStoreIdOrderByCreatedAtDesc(Long storeId);

    List<BusinessInsight> findByInsightTypeAndStoreId(String insightType, Long storeId);
}
