package com.won.smarketing.recommend.infrastructure.persistence;

import com.won.smarketing.recommend.domain.model.MarketingTip;
import com.won.smarketing.recommend.domain.model.StoreData;
import com.won.smarketing.recommend.domain.repository.MarketingTipRepository;
import com.won.smarketing.recommend.domain.service.StoreDataProvider;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Slf4j
@Repository
@RequiredArgsConstructor
public class MarketingTipRepositoryImpl implements MarketingTipRepository {

    private final MarketingTipJpaRepository jpaRepository;
    private final StoreDataProvider storeDataProvider;

    @Override
    public MarketingTip save(MarketingTip marketingTip) {
        String userId = getCurrentUserId();
        MarketingTipEntity entity = MarketingTipEntity.fromDomain(marketingTip, userId);
        MarketingTipEntity savedEntity = jpaRepository.save(entity);

        // Store 정보는 다시 조회해서 Domain에 설정
        StoreData storeData = storeDataProvider.getStoreDataByUserId(userId);
        return savedEntity.toDomain(storeData);
    }

    @Override
    public Optional<MarketingTip> findById(Long tipId) {
        return jpaRepository.findById(tipId)
                .map(entity -> {
                    // Store 정보를 API로 조회
                    StoreData storeData = storeDataProvider.getStoreDataByUserId(entity.getUserId());
                    return entity.toDomain(storeData);
                });
    }

    @Override
    public Page<MarketingTip> findByStoreIdOrderByCreatedAtDesc(Long storeId, Pageable pageable) {
        // 기존 메서드는 호환성을 위해 유지하지만, 내부적으로는 userId로 조회
        String userId = getCurrentUserId();
        return findByUserIdOrderByCreatedAtDesc(userId, pageable);
    }

    /**
     * 사용자별 마케팅 팁 조회 (새로 추가)
     */
    public Page<MarketingTip> findByUserIdOrderByCreatedAtDesc(String userId, Pageable pageable) {
        Page<MarketingTipEntity> entities = jpaRepository.findByUserIdOrderByCreatedAtDesc(userId, pageable);

        // Store 정보는 한 번만 조회 (같은 userId이므로)
        StoreData storeData = storeDataProvider.getStoreDataByUserId(userId);

        return entities.map(entity -> entity.toDomain(storeData));
    }

    /**
     * 사용자의 가장 최근 마케팅 팁 조회
     */
    public Optional<MarketingTip> findMostRecentByUserId(String userId) {
        return jpaRepository.findTopByUserIdOrderByCreatedAtDesc(userId)
                .map(entity -> {
                    StoreData storeData = storeDataProvider.getStoreDataByUserId(userId);
                    return entity.toDomain(storeData);
                });
    }

    /**
     * 특정 팁이 해당 사용자의 것인지 확인
     */
    public boolean isOwnedByUser(Long tipId, String userId) {
        return jpaRepository.existsByIdAndUserId(tipId, userId);
    }

    /**
     * 현재 로그인된 사용자 ID 조회
     */
    private String getCurrentUserId() {
        return SecurityContextHolder.getContext().getAuthentication().getName();
    }
}