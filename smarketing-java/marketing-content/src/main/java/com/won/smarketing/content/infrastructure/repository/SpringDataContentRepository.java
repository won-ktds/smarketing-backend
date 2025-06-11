package com.won.smarketing.content.infrastructure.repository;

import com.won.smarketing.content.infrastructure.entity.ContentJpaEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Spring Data JPA 콘텐츠 Repository
 *
 * @author smarketing-team
 * @version 1.0
 */
@Repository
public interface SpringDataContentRepository extends JpaRepository<ContentJpaEntity, Long> {

    /**
     * 필터 조건으로 콘텐츠를 조회합니다.
     *
     * @param contentType 콘텐츠 타입
     * @param platform 플랫폼
     * @param period 기간
     * @param sortBy 정렬 기준
     * @return 콘텐츠 목록
     */
    @Query("SELECT c FROM ContentJpaEntity c WHERE " +
            "(:contentType IS NULL OR c.contentType = :contentType) AND " +
            "(:platform IS NULL OR c.platform = :platform) AND " +
            "(:period IS NULL OR DATE(c.createdAt) >= CURRENT_DATE - INTERVAL :period DAY) " +
            "ORDER BY " +
            "CASE WHEN :sortBy = 'latest' THEN c.createdAt END DESC, " +
            "CASE WHEN :sortBy = 'oldest' THEN c.createdAt END ASC")
    List<ContentJpaEntity> findByFilters(@Param("contentType") String contentType,
                                         @Param("platform") String platform,
                                         @Param("period") String period,
                                         @Param("sortBy") String sortBy);

    /**
     * 진행 중인 콘텐츠를 조회합니다.
     *
     * @param period 기간
     * @return 진행 중인 콘텐츠 목록
     */
    @Query("SELECT c FROM ContentJpaEntity c " +
            "WHERE c.status = 'PUBLISHED' AND " +
            "(:period IS NULL OR DATE(c.createdAt) >= CURRENT_DATE - INTERVAL :period DAY)")
    List<ContentJpaEntity> findOngoingContents(@Param("period") String period);
}