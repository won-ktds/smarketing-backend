package com.won.smarketing.recommend.domain.repository;

import com.won.smarketing.recommend.domain.model.MarketingTip;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.Optional;

/**
 * 마케팅 팁 레포지토리 인터페이스
 */
public interface MarketingTipRepository {

    MarketingTip save(MarketingTip marketingTip);

    Optional<MarketingTip> findById(Long tipId);

    Page<MarketingTip> findByStoreIdOrderByCreatedAtDesc(Long storeId, Pageable pageable);
}