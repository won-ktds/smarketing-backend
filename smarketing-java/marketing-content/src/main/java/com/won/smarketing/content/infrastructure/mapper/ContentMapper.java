package com.won.smarketing.content.infrastructure.mapper;

import com.won.smarketing.content.domain.model.*;
import com.won.smarketing.content.infrastructure.entity.ContentConditionsJpaEntity;
import com.won.smarketing.content.infrastructure.entity.ContentJpaEntity;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.Collections;
import java.util.List;

/**
 * 콘텐츠 도메인-엔티티 매퍼
 *
 * @author smarketing-team
 * @version 1.0
 */
@Component
@RequiredArgsConstructor
@Slf4j
public class ContentMapper {

    private final ObjectMapper objectMapper;

    /**
     * 도메인 모델을 JPA 엔티티로 변환합니다.
     *
     * @param content 도메인 콘텐츠
     * @return JPA 엔티티
     */
    public ContentJpaEntity toEntity(Content content) {
        if (content == null) {
            return null;
        }

        ContentJpaEntity entity = new ContentJpaEntity();
        if (content.getId() != null) {
            entity.setId(content.getId());
        }
        entity.setStoreId(content.getStoreId());
        entity.setContentType(content.getContentType().name());
        entity.setPlatform(content.getPlatform() != null ? content.getPlatform().name() : null);
        entity.setTitle(content.getTitle());
        entity.setContent(content.getContent());
        entity.setHashtags(convertListToJson(content.getHashtags()));
        entity.setImages(convertListToJson(content.getImages()));
        entity.setStatus(content.getStatus().name());
        entity.setCreatedAt(content.getCreatedAt());
        entity.setUpdatedAt(content.getUpdatedAt());

        // 조건 정보 매핑
        if (content.getCreationConditions() != null) {
            ContentConditionsJpaEntity conditionsEntity = new ContentConditionsJpaEntity();
            conditionsEntity.setContent(entity);
            conditionsEntity.setCategory(content.getCreationConditions().getCategory());
            conditionsEntity.setRequirement(content.getCreationConditions().getRequirement());
            conditionsEntity.setToneAndManner(content.getCreationConditions().getToneAndManner());
            conditionsEntity.setEmotionIntensity(content.getCreationConditions().getEmotionIntensity());
            conditionsEntity.setEventName(content.getCreationConditions().getEventName());
            conditionsEntity.setStartDate(content.getCreationConditions().getStartDate());
            conditionsEntity.setEndDate(content.getCreationConditions().getEndDate());
            conditionsEntity.setPhotoStyle(content.getCreationConditions().getPhotoStyle());
            entity.setConditions(conditionsEntity);
        }

        return entity;
    }

    /**
     * JPA 엔티티를 도메인 모델로 변환합니다.
     *
     * @param entity JPA 엔티티
     * @return 도메인 콘텐츠
     */
    public Content toDomain(ContentJpaEntity entity) {
        if (entity == null) {
            return null;
        }

        CreationConditions conditions = null;
        if (entity.getConditions() != null) {
            conditions = new CreationConditions(
                    entity.getConditions().getCategory(),
                    entity.getConditions().getRequirement(),
                    entity.getConditions().getToneAndManner(),
                    entity.getConditions().getEmotionIntensity(),
                    entity.getConditions().getEventName(),
                    entity.getConditions().getStartDate(),
                    entity.getConditions().getEndDate(),
                    entity.getConditions().getPhotoStyle(),
                  //  entity.getConditions().getTargetAudience(),
                    entity.getConditions().getPromotionType()
            );
        }

        return new Content(
                ContentId.of(entity.getId()),
                ContentType.valueOf(entity.getContentType()),
                entity.getPlatform() != null ? Platform.valueOf(entity.getPlatform()) : null,
                entity.getTitle(),
                entity.getContent(),
                convertJsonToList(entity.getHashtags()),
                convertJsonToList(entity.getImages()),
                ContentStatus.valueOf(entity.getStatus()),
                conditions,
                entity.getStoreId(),
                entity.getCreatedAt(),
                entity.getUpdatedAt()
        );
    }

    /**
     * List를 JSON 문자열로 변환합니다.
     */
    private String convertListToJson(List<String> list) {
        if (list == null || list.isEmpty()) {
            return null;
        }
        try {
            return objectMapper.writeValueAsString(list);
        } catch (Exception e) {
            log.warn("Failed to convert list to JSON: {}", e.getMessage());
            return null;
        }
    }

    /**
     * JSON 문자열을 List로 변환합니다.
     */
    private List<String> convertJsonToList(String json) {
        if (json == null || json.trim().isEmpty()) {
            return Collections.emptyList();
        }
        try {
            return objectMapper.readValue(json, new TypeReference<List<String>>() {});
        } catch (Exception e) {
            log.warn("Failed to convert JSON to list: {}", e.getMessage());
            return Collections.emptyList();
        }
    }
}
