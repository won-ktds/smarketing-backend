// marketing-content/src/main/java/com/won/smarketing/content/infrastructure/repository/JpaContentRepository.java
package com.won.smarketing.content.infrastructure.repository;

import com.won.smarketing.content.domain.model.Content;
import com.won.smarketing.content.domain.model.ContentId;
import com.won.smarketing.content.domain.model.ContentType;
import com.won.smarketing.content.domain.model.Platform;
import com.won.smarketing.content.domain.repository.ContentRepository;
import com.won.smarketing.content.infrastructure.entity.ContentJpaEntity;
import com.won.smarketing.content.infrastructure.mapper.ContentMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * JPA를 활용한 콘텐츠 리포지토리 구현체
 * Clean Architecture의 Infrastructure Layer에 위치
 * JPA 엔티티와 도메인 모델 간 변환을 위해 ContentMapper 사용
 */
@Repository
@RequiredArgsConstructor
@Slf4j
public class JpaContentRepository implements ContentRepository {

    private final JpaContentRepositoryInterface jpaRepository;
    private final ContentMapper contentMapper;

    /**
     * 콘텐츠 저장
     * @param content 저장할 도메인 콘텐츠
     * @return 저장된 도메인 콘텐츠
     */
    @Override
    public Content save(Content content) {
        log.debug("Saving content: {}", content.getTitle());

        // 도메인 모델을 JPA 엔티티로 변환
        ContentJpaEntity entity = contentMapper.toEntity(content);

        // JPA로 저장
        ContentJpaEntity savedEntity = jpaRepository.save(entity);

        // JPA 엔티티를 도메인 모델로 변환하여 반환
        Content savedContent = contentMapper.toDomain(savedEntity);

        log.debug("Content saved with ID: {}", savedContent.getId());
        return savedContent;
    }

    /**
     * ID로 콘텐츠 조회
     * @param id 콘텐츠 ID
     * @return 조회된 도메인 콘텐츠
     */
    @Override
    public Optional<Content> findById(ContentId id) {
        log.debug("Finding content by ID: {}", id.getValue());

        return jpaRepository.findById(id.getValue())
                .map(contentMapper::toDomain);
    }

    /**
     * 필터 조건으로 콘텐츠 목록 조회
     * @param contentType 콘텐츠 타입
     * @param platform 플랫폼
     * @param period 기간 (현재는 사용하지 않음)
     * @param sortBy 정렬 기준 (현재는 사용하지 않음)
     * @return 도메인 콘텐츠 목록
     */
    @Override
    public List<Content> findByFilters(ContentType contentType, Platform platform, String period, String sortBy) {
        log.debug("Finding contents with filters - contentType: {}, platform: {}", contentType, platform);

        String contentTypeStr = contentType != null ? contentType.name() : null;
        String platformStr = platform != null ? platform.name() : null;

        List<ContentJpaEntity> entities = jpaRepository.findByFilters(contentTypeStr, platformStr, null);

        return entities.stream()
                .map(contentMapper::toDomain)
                .collect(Collectors.toList());
    }

    /**
     * 진행 중인 콘텐츠 목록 조회
     * @param period 기간 (현재는 사용하지 않음)
     * @return 진행 중인 도메인 콘텐츠 목록
     */
    @Override
    public List<Content> findOngoingContents(String period) {
        log.debug("Finding ongoing contents");

        List<ContentJpaEntity> entities = jpaRepository.findOngoingContents();

        return entities.stream()
                .map(contentMapper::toDomain)
                .collect(Collectors.toList());
    }

    /**
     * ID로 콘텐츠 삭제
     * @param id 삭제할 콘텐츠 ID
     */
    @Override
    public void deleteById(ContentId id) {
        log.debug("Deleting content by ID: {}", id.getValue());

        jpaRepository.deleteById(id.getValue());

        log.debug("Content deleted successfully");
    }

    /**
     * 매장 ID로 콘텐츠 목록 조회 (추가 메서드)
     * @param storeId 매장 ID
     * @return 도메인 콘텐츠 목록
     */
    public List<Content> findByStoreId(Long storeId) {
        log.debug("Finding contents by store ID: {}", storeId);

        List<ContentJpaEntity> entities = jpaRepository.findByStoreId(storeId);

        return entities.stream()
                .map(contentMapper::toDomain)
                .collect(Collectors.toList());
    }

    /**
     * 콘텐츠 타입으로 조회 (추가 메서드)
     * @param contentType 콘텐츠 타입
     * @return 도메인 콘텐츠 목록
     */
    public List<Content> findByContentType(ContentType contentType) {
        log.debug("Finding contents by type: {}", contentType);

        List<ContentJpaEntity> entities = jpaRepository.findByContentType(contentType.name());

        return entities.stream()
                .map(contentMapper::toDomain)
                .collect(Collectors.toList());
    }
}