package com.won.smarketing.content.application.service;

import com.won.smarketing.content.application.usecase.SnsContentUseCase;
import com.won.smarketing.content.domain.model.Content;
import com.won.smarketing.content.domain.model.ContentId;
import com.won.smarketing.content.domain.model.ContentStatus;
import com.won.smarketing.content.domain.model.ContentType;
import com.won.smarketing.content.domain.model.CreationConditions;
import com.won.smarketing.content.domain.model.Platform;
import com.won.smarketing.content.domain.repository.ContentRepository;
import com.won.smarketing.content.domain.service.AiContentGenerator;
import com.won.smarketing.content.presentation.dto.SnsContentCreateRequest;
import com.won.smarketing.content.presentation.dto.SnsContentCreateResponse;
import com.won.smarketing.content.presentation.dto.SnsContentSaveRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

/**
 * SNS 콘텐츠 서비스 구현체
 * SNS 게시물 생성 및 저장 기능 구현
 */
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class SnsContentService implements SnsContentUseCase {

    private final ContentRepository contentRepository;
    private final AiContentGenerator aiContentGenerator;

    /**
     * SNS 콘텐츠 생성
     *
     * @param request SNS 콘텐츠 생성 요청
     * @return 생성된 SNS 콘텐츠 정보
     */
    @Override
    @Transactional
    public SnsContentCreateResponse generateSnsContent(SnsContentCreateRequest request) {
        // AI를 사용하여 SNS 콘텐츠 생성
        String generatedContent = aiContentGenerator.generateSnsContent(request);

        // 플랫폼에 맞는 해시태그 생성
        Platform platform = Platform.fromString(request.getPlatform());
        List<String> hashtags = aiContentGenerator.generateHashtags(generatedContent, platform);

        // 생성 조건 정보 구성
        CreationConditions conditions = CreationConditions.builder()
                .category(request.getCategory())
                .requirement(request.getRequirement())
                .toneAndManner(request.getToneAndManner())
                .emotionIntensity(request.getEmotionIntensity())
                .eventName(request.getEventName())
                .startDate(request.getStartDate())
                .endDate(request.getEndDate())
                .build();

        // 임시 콘텐츠 생성 (저장하지 않음)
        Content content = Content.builder()
//                .contentType(ContentType.SNS_POST)
                .platform(platform)
                .title(request.getTitle())
                .content(generatedContent)
                .hashtags(hashtags)
                .images(request.getImages())
                .status(ContentStatus.DRAFT)
                .creationConditions(conditions)
                .storeId(request.getStoreId())
                .createdAt(LocalDateTime.now())
                .updatedAt(LocalDateTime.now())
                .build();

        return SnsContentCreateResponse.builder()
                .contentId(null) // 임시 생성이므로 ID 없음
                .contentType(content.getContentType().name())
                .platform(content.getPlatform().name())
                .title(content.getTitle())
                .content(content.getContent())
                .hashtags(content.getHashtags())
                .fixedImages(content.getImages())
                .status(content.getStatus().name())
                .createdAt(content.getCreatedAt())
                .build();
    }

    /**
     * SNS 콘텐츠 저장
     *
     * @param request SNS 콘텐츠 저장 요청
     */
    @Override
    @Transactional
    public void saveSnsContent(SnsContentSaveRequest request) {
        // 생성 조건 정보 구성
        CreationConditions conditions = CreationConditions.builder()
                .category(request.getCategory())
                .requirement(request.getRequirement())
                .toneAndManner(request.getToneAndManner())
                .emotionIntensity(request.getEmotionIntensity())
                .eventName(request.getEventName())
                .startDate(request.getStartDate())
                .endDate(request.getEndDate())
                .build();

        // 콘텐츠 엔티티 생성 및 저장
        Content content = Content.builder()
//                .contentType(ContentType.SNS_POST)
                .platform(Platform.fromString(request.getPlatform()))
                .title(request.getTitle())
                .content(request.getContent())
                .hashtags(request.getHashtags())
                .images(request.getImages())
                .status(ContentStatus.PUBLISHED)
                .creationConditions(conditions)
                .storeId(request.getStoreId())
                .createdAt(LocalDateTime.now())
                .updatedAt(LocalDateTime.now())
                .build();

        contentRepository.save(content);
    }
}
