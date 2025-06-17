package com.won.smarketing.content.domain.repository;
import com.won.smarketing.content.infrastructure.entity.ContentEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Spring Data JPA ContentRepository
 * JPA 기반 콘텐츠 데이터 접근
 */
@Repository
public interface SpringDataContentRepository extends JpaRepository<ContentEntity, Long> {

    /**
     * 매장별 콘텐츠 조회
     *
     * @param storeId 매장 ID
     * @return 콘텐츠 목록
     */
    List<ContentEntity> findByStoreId(Long storeId);

    /**
     * 콘텐츠 타입별 조회
     *
     * @param contentType 콘텐츠 타입
     * @return 콘텐츠 목록
     */
    List<ContentEntity> findByContentType(String contentType);

    /**
     * 플랫폼별 조회
     *
     * @param platform 플랫폼
     * @return 콘텐츠 목록
     */
    List<ContentEntity> findByPlatform(String platform);
}
