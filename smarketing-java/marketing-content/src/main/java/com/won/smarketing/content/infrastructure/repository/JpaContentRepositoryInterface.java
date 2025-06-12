// marketing-content/src/main/java/com/won/smarketing/content/infrastructure/repository/JpaContentRepositoryInterface.java
package com.won.smarketing.content.infrastructure.repository;

import com.won.smarketing.content.domain.model.Content;
import com.won.smarketing.content.domain.model.ContentType;
import com.won.smarketing.content.domain.model.Platform;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

/**
 * Spring Data JPA 콘텐츠 리포지토리 인터페이스
 * Clean Architecture의 Infrastructure Layer에 위치
 */
public interface JpaContentRepositoryInterface extends JpaRepository<Content, Long> {

    /**
     * 필터 조건으로 콘텐츠 목록 조회
     */
    @Query("SELECT c FROM Content c WHERE " +
            "(:contentType IS NULL OR c.contentType = :contentType) AND " +
            "(:platform IS NULL OR c.platform = :platform) AND " +
            "(:period IS NULL OR " +
            "  (:period = 'week' AND c.createdAt >= CURRENT_DATE - 7) OR " +
            "  (:period = 'month' AND c.createdAt >= CURRENT_DATE - 30) OR " +
            "  (:period = 'year' AND c.createdAt >= CURRENT_DATE - 365)) " +
            "ORDER BY " +
            "CASE WHEN :sortBy = 'latest' THEN c.createdAt END DESC, " +
            "CASE WHEN :sortBy = 'oldest' THEN c.createdAt END ASC, " +
            "CASE WHEN :sortBy = 'title' THEN c.title END ASC")
    List<Content> findByFilters(@Param("contentType") ContentType contentType,
                                @Param("platform") Platform platform,
                                @Param("period") String period,
                                @Param("sortBy") String sortBy);

    /**
     * 진행 중인 콘텐츠 목록 조회
     */
    @Query("SELECT c FROM Content c WHERE " +
            "c.status IN ('PUBLISHED', 'SCHEDULED') AND " +
            "(:period IS NULL OR " +
            "  (:period = 'week' AND c.createdAt >= CURRENT_DATE - 7) OR " +
            "  (:period = 'month' AND c.createdAt >= CURRENT_DATE - 30) OR " +
            "  (:period = 'year' AND c.createdAt >= CURRENT_DATE - 365)) " +
            "ORDER BY c.createdAt DESC")
    List<Content> findOngoingContents(@Param("period") String period);
}