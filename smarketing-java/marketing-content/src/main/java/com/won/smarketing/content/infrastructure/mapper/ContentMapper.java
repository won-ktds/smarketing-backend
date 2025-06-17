// marketing-content/src/main/java/com/won/smarketing/content/infrastructure/mapper/ContentMapper.java
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
 * Clean Architecture에서 Infrastructure Layer와 Domain Layer 간 변환 담당
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
     * 도메인 모델을 JPA 엔티티로 변환
     *
     * @param content 도메인 콘텐츠
     * @return JPA 엔티티
     */
    public ContentJpaEntity toEntity(Content content) {
        if (content == null) {
            return null;
        }

        ContentJpaEntity entity = new ContentJpaEntity();

        // 기본 필드 매핑
//        if (content.getId() != null) {
//            entity.setId(content.getId());
//        }
        entity.setStoreId(content.getStoreId());
        entity.setContentType(content.getContentType() != null ? content.getContentType().name() : null);
        entity.setPlatform(content.getPlatform() != null ? content.getPlatform().name() : null);
        entity.setTitle(content.getTitle());
        entity.setContent(content.getContent());
        entity.setStatus(content.getStatus() != null ? content.getStatus().name() : "DRAFT");
        entity.setPromotionStartDate(content.getPromotionStartDate());
        entity.setPromotionEndDate(content.getPromotionEndDate());
        entity.setCreatedAt(content.getCreatedAt());
        entity.setUpdatedAt(content.getUpdatedAt());

        // 컬렉션 필드를 JSON으로 변환
        entity.setHashtags(convertListToJson(content.getHashtags()));
        entity.setImages(convertListToJson(content.getImages()));

        // 생성 조건 정보 매핑
        if (content.getCreationConditions() != null) {
            ContentConditionsJpaEntity conditionsEntity = mapToConditionsEntity(content.getCreationConditions());
            conditionsEntity.setContent(entity);
            entity.setConditions(conditionsEntity);
        }

        return entity;
    }

    /**
     * JPA 엔티티를 도메인 모델로 변환
     *
     * @param entity JPA 엔티티
     * @return 도메인 모델
     */
    public Content toDomain(ContentJpaEntity entity) {
        if (entity == null) {
            return null;
        }

        return Content.builder()
                .id(entity.getId())
                .storeId(entity.getStoreId())
                .contentType(parseContentType(entity.getContentType()))
                .platform(parsePlatform(entity.getPlatform()))
                .title(entity.getTitle())
                .content(entity.getContent())
                .hashtags(convertJsonToList(entity.getHashtags()))
                .images(convertJsonToList(entity.getImages()))
                .status(parseContentStatus(entity.getStatus()))
                .promotionStartDate(entity.getPromotionStartDate())
                .promotionEndDate(entity.getPromotionEndDate())
                .creationConditions(mapToConditionsDomain(entity.getConditions()))
                .createdAt(entity.getCreatedAt())
                .updatedAt(entity.getUpdatedAt())
                .build();
    }

    /**
     * CreationConditions 도메인을 JPA 엔티티로 변환
     */
    private ContentConditionsJpaEntity mapToConditionsEntity(CreationConditions conditions) {
        ContentConditionsJpaEntity entity = new ContentConditionsJpaEntity();
        entity.setCategory(conditions.getCategory());
        entity.setRequirement(conditions.getRequirement());
//        entity.setToneAndManner(conditions.getToneAndManner());
//        entity.setEmotionIntensity(conditions.getEmotionIntensity());
        entity.setEventName(conditions.getEventName());
        entity.setStartDate(conditions.getStartDate());
        entity.setEndDate(conditions.getEndDate());
        entity.setPhotoStyle(conditions.getPhotoStyle());
        entity.setPromotionType(conditions.getPromotionType());
        return entity;
    }

    /**
     * CreationConditions JPA 엔티티를 도메인으로 변환
     */
    private CreationConditions mapToConditionsDomain(ContentConditionsJpaEntity entity) {
        if (entity == null) {
            return null;
        }

        return CreationConditions.builder()
                .category(entity.getCategory())
                .requirement(entity.getRequirement())
//                .toneAndManner(entity.getToneAndManner())
//                .emotionIntensity(entity.getEmotionIntensity())
                .eventName(entity.getEventName())
                .startDate(entity.getStartDate())
                .endDate(entity.getEndDate())
                .photoStyle(entity.getPhotoStyle())
                .promotionType(entity.getPromotionType())
                .build();
    }

    /**
     * List를 JSON 문자열로 변환
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
     * JSON 문자열을 List로 변환
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

    /**
     * 문자열을 ContentType 열거형으로 변환
     */
    private ContentType parseContentType(String contentType) {
        if (contentType == null) {
            return null;
        }
        try {
            return ContentType.valueOf(contentType);
        } catch (IllegalArgumentException e) {
            log.warn("Unknown content type: {}", contentType);
            return null;
        }
    }

    /**
     * 문자열을 Platform 열거형으로 변환
     */
    private Platform parsePlatform(String platform) {
        if (platform == null) {
            return null;
        }
        try {
            return Platform.valueOf(platform);
        } catch (IllegalArgumentException e) {
            log.warn("Unknown platform: {}", platform);
            return null;
        }
    }

    /**
     * 문자열을 ContentStatus 열거형으로 변환
     */
    private ContentStatus parseContentStatus(String status) {
        if (status == null) {
            return ContentStatus.DRAFT;
        }
        try {
            return ContentStatus.valueOf(status);
        } catch (IllegalArgumentException e) {
            log.warn("Unknown content status: {}", status);
            return ContentStatus.DRAFT;
        }
    }
}