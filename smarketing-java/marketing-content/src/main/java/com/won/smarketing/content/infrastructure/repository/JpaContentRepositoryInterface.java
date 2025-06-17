// marketing-content/src/main/java/com/won/smarketing/content/infrastructure/repository/JpaContentRepositoryInterface.java
package com.won.smarketing.content.infrastructure.repository;

import com.won.smarketing.content.infrastructure.entity.ContentJpaEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

/**
 * Spring Data JPA 콘텐츠 리포지토리 인터페이스
 * Clean Architecture의 Infrastructure Layer에 위치
 * JPA 엔티티(ContentJpaEntity)를 사용하여 데이터베이스 접근
 */
public interface JpaContentRepositoryInterface extends JpaRepository<ContentJpaEntity, Long> {

    /**
     * 매장 ID로 콘텐츠 목록 조회
     * @param storeId 매장 ID
     * @return 콘텐츠 엔티티 목록
     */
    List<ContentJpaEntity> findByStoreId(Long storeId);

    /**
     * 콘텐츠 타입으로 조회
     * @param contentType 콘텐츠 타입
     * @return 콘텐츠 엔티티 목록
     */
    List<ContentJpaEntity> findByContentType(String contentType);

    /**
     * 플랫폼으로 조회
     * @param platform 플랫폼
     * @return 콘텐츠 엔티티 목록
     */
    List<ContentJpaEntity> findByPlatform(String platform);

    /**
     * 상태로 조회
     * @param status 상태
     * @return 콘텐츠 엔티티 목록
     */
    List<ContentJpaEntity> findByStatus(String status);

    /**
     * 필터 조건으로 콘텐츠 목록 조회
     * @param storeId 콘텐츠 타입
     * @param platform 플랫폼 (null 가능)
     * @return 콘텐츠 엔티티 목록
     */
    @Query("SELECT c FROM ContentJpaEntity c WHERE " +
            "(c.storeId = :storeId) AND " +
            "(:platform IS NULL OR c.platform = :platform)" +
            "ORDER BY c.createdAt DESC")
    List<ContentJpaEntity> findByFilters(@Param("storeId") Long storeId,
                                         @Param("platform") String platform);

    /**
     * 진행 중인 콘텐츠 목록 조회 (발행된 상태의 콘텐츠)
     * @return 진행 중인 콘텐츠 엔티티 목록
     */
    @Query("SELECT c FROM ContentJpaEntity c WHERE " +
            "c.status IN ('PUBLISHED', 'SCHEDULED') " +
            "ORDER BY c.createdAt DESC")
    List<ContentJpaEntity> findOngoingContents();

    /**
     * 매장 ID와 콘텐츠 타입으로 조회
     * @param storeId 매장 ID
     * @param contentType 콘텐츠 타입
     * @return 콘텐츠 엔티티 목록
     */
    List<ContentJpaEntity> findByStoreIdAndContentType(Long storeId, String contentType);

    /**
     * 최근 생성된 콘텐츠 조회 (limit 적용)
     * @param storeId 매장 ID
     * @return 최근 콘텐츠 엔티티 목록
     */
    @Query("SELECT c FROM ContentJpaEntity c WHERE c.storeId = :storeId " +
            "ORDER BY c.createdAt DESC")
    List<ContentJpaEntity> findRecentContentsByStoreId(@Param("storeId") Long storeId);
}