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
 * JPA 기반 콘텐츠 Repository 구현체
 *
 * @author smarketing-team
 * @version 1.0
 */
@Repository
@RequiredArgsConstructor
@Slf4j
public class JpaContentRepository implements ContentRepository {

    private final SpringDataContentRepository springDataContentRepository;
    private final ContentMapper contentMapper;

    /**
     * 콘텐츠를 저장합니다.
     *
     * @param content 저장할 콘텐츠
     * @return 저장된 콘텐츠
     */
    @Override
    public Content save(Content content) {
        log.debug("Saving content: {}", content.getId());
        ContentJpaEntity entity = contentMapper.toEntity(content);
        ContentJpaEntity savedEntity = springDataContentRepository.save(entity);
        return contentMapper.toDomain(savedEntity);
    }

    /**
     * ID로 콘텐츠를 조회합니다.
     *
     * @param id 콘텐츠 ID
     * @return 조회된 콘텐츠
     */
    @Override
    public Optional<Content> findById(ContentId id) {
        log.debug("Finding content by id: {}", id.getValue());
        return springDataContentRepository.findById(id.getValue())
                .map(contentMapper::toDomain);
    }

    /**
     * 필터 조건으로 콘텐츠 목록을 조회합니다.
     *
     * @param contentType 콘텐츠 타입
     * @param platform 플랫폼
     * @param period 기간
     * @param sortBy 정렬 기준
     * @return 콘텐츠 목록
     */
    @Override
    public List<Content> findByFilters(ContentType contentType, Platform platform, String period, String sortBy) {
        log.debug("Finding contents by filters - type: {}, platform: {}, period: {}, sortBy: {}",
                contentType, platform, period, sortBy);

        List<ContentJpaEntity> entities = springDataContentRepository.findByFilters(
                contentType != null ? contentType.name() : null,
                platform != null ? platform.name() : null,
                period,
                sortBy
        );

        return entities.stream()
                .map(contentMapper::toDomain)
                .collect(Collectors.toList());
    }

    /**
     * 진행 중인 콘텐츠 목록을 조회합니다.
     *
     * @param period 기간
     * @return 진행 중인 콘텐츠 목록
     */
    @Override
    public List<Content> findOngoingContents(String period) {
        log.debug("Finding ongoing contents for period: {}", period);
        List<ContentJpaEntity> entities = springDataContentRepository.findOngoingContents(period);

        return entities.stream()
                .map(contentMapper::toDomain)
                .collect(Collectors.toList());
    }

    /**
     * ID로 콘텐츠를 삭제합니다.
     *
     * @param id 콘텐츠 ID
     */
    @Override
    public void deleteById(ContentId id) {
        log.debug("Deleting content by id: {}", id.getValue());
        springDataContentRepository.deleteById(id.getValue());
    }
}