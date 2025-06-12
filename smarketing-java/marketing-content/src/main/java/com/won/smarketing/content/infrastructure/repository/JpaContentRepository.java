// marketing-content/src/main/java/com/won/smarketing/content/infrastructure/repository/JpaContentRepository.java
package com.won.smarketing.content.infrastructure.repository;

import com.won.smarketing.content.domain.model.Content;
import com.won.smarketing.content.domain.model.ContentId;
import com.won.smarketing.content.domain.model.ContentType;
import com.won.smarketing.content.domain.model.Platform;
import com.won.smarketing.content.domain.repository.ContentRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * JPA를 활용한 콘텐츠 리포지토리 구현체
 * Clean Architecture의 Infrastructure Layer에 위치
 */
@Repository
@RequiredArgsConstructor
public class JpaContentRepository implements ContentRepository {

    private final JpaContentRepositoryInterface jpaRepository;

    /**
     * 콘텐츠 저장
     * @param content 저장할 콘텐츠
     * @return 저장된 콘텐츠
     */
    @Override
    public Content save(Content content) {
        return jpaRepository.save(content);
    }

    /**
     * ID로 콘텐츠 조회
     * @param id 콘텐츠 ID
     * @return 조회된 콘텐츠
     */
    @Override
    public Optional<Content> findById(ContentId id) {
        return jpaRepository.findById(id.getValue());
    }

    /**
     * 필터 조건으로 콘텐츠 목록 조회
     * @param contentType 콘텐츠 타입
     * @param platform 플랫폼
     * @param period 기간
     * @param sortBy 정렬 기준
     * @return 콘텐츠 목록
     */
    @Override
    public List<Content> findByFilters(ContentType contentType, Platform platform, String period, String sortBy) {
        return jpaRepository.findByFilters(contentType, platform, period, sortBy);
    }

    /**
     * 진행 중인 콘텐츠 목록 조회
     * @param period 기간
     * @return 진행 중인 콘텐츠 목록
     */
    @Override
    public List<Content> findOngoingContents(String period) {
        return jpaRepository.findOngoingContents(period);
    }

    /**
     * ID로 콘텐츠 삭제
     * @param id 삭제할 콘텐츠 ID
     */
    @Override
    public void deleteById(ContentId id) {
        jpaRepository.deleteById(id.getValue());
    }
}