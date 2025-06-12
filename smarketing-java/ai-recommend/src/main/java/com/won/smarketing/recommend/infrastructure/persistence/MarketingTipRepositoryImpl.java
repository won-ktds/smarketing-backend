package com.won.smarketing.recommend.infrastructure.persistence;

import com.won.smarketing.recommend.domain.model.MarketingTip;
import com.won.smarketing.recommend.domain.repository.MarketingTipRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * 마케팅 팁 레포지토리 구현체
 */
@Repository
@RequiredArgsConstructor
public class MarketingTipRepositoryImpl implements MarketingTipRepository {

    private final MarketingTipJpaRepository jpaRepository;

    @Override
    public MarketingTip save(MarketingTip marketingTip) {
        MarketingTipEntity entity = MarketingTipEntity.fromDomain(marketingTip);
        MarketingTipEntity savedEntity = jpaRepository.save(entity);
        return savedEntity.toDomain();
    }

    @Override
    public Optional<MarketingTip> findById(Long tipId) {
        return jpaRepository.findById(tipId)
                .map(MarketingTipEntity::toDomain);
    }

    @Override
    public Page<MarketingTip> findByStoreIdOrderByCreatedAtDesc(Long storeId, Pageable pageable) {
        return jpaRepository.findByStoreIdOrderByCreatedAtDesc(storeId, pageable)
                .map(MarketingTipEntity::toDomain);
    }
}