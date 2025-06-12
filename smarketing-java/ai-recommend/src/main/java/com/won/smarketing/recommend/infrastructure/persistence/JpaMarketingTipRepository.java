import com.won.smarketing.recommend.domain.model.MarketingTip;
import com.won.smarketing.recommend.domain.repository.MarketingTipRepository;
import com.won.smarketing.recommend.infrastructure.persistence.MarketingTipJpaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * JPA 마케팅 팁 레포지토리 구현체
 */
@Repository
@RequiredArgsConstructor
public class JpaMarketingTipRepository implements MarketingTipRepository {

    private final MarketingTipJpaRepository jpaRepository;

    @Override
    public MarketingTip save(MarketingTip marketingTip) {
        com.won.smarketing.recommend.entity.MarketingTipEntity entity = MarketingTipEntity.fromDomain(marketingTip);
        com.won.smarketing.recommend.entity.MarketingTipEntity savedEntity = jpaRepository.save(entity);
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