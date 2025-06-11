package com.won.smarketing.content.application.service;

import com.won.smarketing.common.exception.BusinessException;
import com.won.smarketing.common.exception.ErrorCode;
import com.won.smarketing.content.application.usecase.ContentQueryUseCase;
import com.won.smarketing.content.domain.model.*;
import com.won.smarketing.content.domain.repository.ContentRepository;
import com.won.smarketing.content.presentation.dto.*;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;
import java.util.stream.Collectors;

/**
 * 콘텐츠 조회 서비스 구현체
 * 콘텐츠 수정, 조회, 삭제 기능 구현
 */
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class ContentQueryService implements ContentQueryUseCase {

    private final ContentRepository contentRepository;

    /**
     * 콘텐츠 수정
     * 
     * @param contentId 수정할 콘텐츠 ID
     * @param request 콘텐츠 수정 요청
     * @return 수정된 콘텐츠 정보
     */
    @Override
    @Transactional
    public ContentUpdateResponse updateContent(Long contentId, ContentUpdateRequest request) {
        Content content = contentRepository.findById(ContentId.of(contentId))
                .orElseThrow(() -> new BusinessException(ErrorCode.CONTENT_NOT_FOUND));

        // 제목과 기간 업데이트
        content.updateTitle(request.getTitle());
        content.updatePeriod(request.getStartDate(), request.getEndDate());

        Content updatedContent = contentRepository.save(content);

        return ContentUpdateResponse.builder()
                .contentId(updatedContent.getId().getValue())
                .contentType(updatedContent.getContentType().name())
                .platform(updatedContent.getPlatform().name())
                .title(updatedContent.getTitle())
                .content(updatedContent.getContent())
                .hashtags(updatedContent.getHashtags())
                .images(updatedContent.getImages())
                .status(updatedContent.getStatus().name())
                .updatedAt(updatedContent.getUpdatedAt())
                .build();
    }

    /**
     * 콘텐츠 목록 조회
     * 
     * @param contentType 콘텐츠 타입
     * @param platform 플랫폼
     * @param period 기간
     * @param sortBy 정렬 기준
     * @return 콘텐츠 목록
     */
    @Override
    public List<ContentResponse> getContents(String contentType, String platform, String period, String sortBy) {
        ContentType type = contentType != null ? ContentType.fromString(contentType) : null;
        Platform platformEnum = platform != null ? Platform.fromString(platform) : null;
        
        List<Content> contents = contentRepository.findByFilters(type, platformEnum, period, sortBy);

        return contents.stream()
                .map(this::toContentResponse)
                .collect(Collectors.toList());
    }

    /**
     * 진행 중인 콘텐츠 목록 조회
     * 
     * @param period 기간
     * @return 진행 중인 콘텐츠 목록
     */
    @Override
    public List<OngoingContentResponse> getOngoingContents(String period) {
        List<Content> contents = contentRepository.findOngoingContents(period);

        return contents.stream()
                .map(this::toOngoingContentResponse)
                .collect(Collectors.toList());
    }

    /**
     * 콘텐츠 상세 조회
     * 
     * @param contentId 콘텐츠 ID
     * @return 콘텐츠 상세 정보
     */
    @Override
    public ContentDetailResponse getContentDetail(Long contentId) {
        Content content = contentRepository.findById(ContentId.of(contentId))
                .orElseThrow(() -> new BusinessException(ErrorCode.CONTENT_NOT_FOUND));

        return ContentDetailResponse.builder()
                .contentId(content.getId().getValue())
                .contentType(content.getContentType().name())
                .platform(content.getPlatform().name())
                .title(content.getTitle())
                .content(content.getContent())
                .hashtags(content.getHashtags())
                .images(content.getImages())
                .status(content.getStatus().name())
                .creationConditions(toCreationConditionsDto(content.getCreationConditions()))
                .createdAt(content.getCreatedAt())
                .build();
    }

    /**
     * 콘텐츠 삭제
     * 
     * @param contentId 삭제할 콘텐츠 ID
     */
    @Override
    @Transactional
    public void deleteContent(Long contentId) {
        Content content = contentRepository.findById(ContentId.of(contentId))
                .orElseThrow(() -> new BusinessException(ErrorCode.CONTENT_NOT_FOUND));
        
        contentRepository.deleteById(ContentId.of(contentId));
    }

    /**
     * Content 엔티티를 ContentResponse DTO로 변환
     * 
     * @param content Content 엔티티
     * @return ContentResponse DTO
     */
    private ContentResponse toContentResponse(Content content) {
        return ContentResponse.builder()
                .contentId(content.getId().getValue())
                .contentType(content.getContentType().name())
                .platform(content.getPlatform().name())
                .title(content.getTitle())
                .content(content.getContent())
                .hashtags(content.getHashtags())
                .images(content.getImages())
                .status(content.getStatus().name())
                .createdAt(content.getCreatedAt())
                .viewCount(0) // TODO: 실제 조회 수 구현 필요
                .build();
    }

    /**
     * Content 엔티티를 OngoingContentResponse DTO로 변환
     * 
     * @param content Content 엔티티
     * @return OngoingContentResponse DTO
     */
    private OngoingContentResponse toOngoingContentResponse(Content content) {
        return OngoingContentResponse.builder()
                .contentId(content.getId().getValue())
                .contentType(content.getContentType().name())
                .platform(content.getPlatform().name())
                .title(content.getTitle())
                .status(content.getStatus().name())
                .createdAt(content.getCreatedAt())
                .viewCount(0) // TODO: 실제 조회 수 구현 필요
                .build();
    }

    /**
     * CreationConditions를 DTO로 변환
     * 
     * @param conditions CreationConditions 도메인 객체
     * @return CreationConditionsDto
     */
    private ContentDetailResponse.CreationConditionsDto toCreationConditionsDto(CreationConditions conditions) {
        if (conditions == null) {
            return null;
        }
        
        return ContentDetailResponse.CreationConditionsDto.builder()
                .toneAndManner(conditions.getToneAndManner())
                .emotionIntensity(conditions.getEmotionIntensity())
                .eventName(conditions.getEventName())
                .build();
    }
}
