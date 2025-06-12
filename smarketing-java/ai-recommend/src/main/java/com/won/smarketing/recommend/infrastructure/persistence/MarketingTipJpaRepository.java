import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

/**
 * 마케팅 팁 JPA 레포지토리
 */
public interface MarketingTipJpaRepository extends JpaRepository<com.won.smarketing.recommend.entity.MarketingTipEntity, Long> {

    @Query("SELECT m FROM MarketingTipEntity m WHERE m.storeId = :storeId ORDER BY m.createdAt DESC")
    Page<com.won.smarketing.recommend.entity.MarketingTipEntity> findByStoreIdOrderByCreatedAtDesc(@Param("storeId") Long storeId, Pageable pageable);
}