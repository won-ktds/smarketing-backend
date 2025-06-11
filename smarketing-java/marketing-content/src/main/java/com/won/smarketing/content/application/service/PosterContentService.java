package com.won.smarketing.content.application.service;

import com.won.smarketing.content.application.usecase.PosterContentUseCase;
import com.won.smarketing.content.domain.model.Content;
import com.won.smarketing.content.domain.model.ContentStatus;
import com.won.smarketing.content.domain.model.ContentType;
import com.won.smarketing.content.domain.model.CreationConditions;
import com.won.smarketing.content.domain.model.Platform;
import com.won.smarketing.content.domain.repository.ContentRepository;
import com.won.smarketing.content.domain.service.AiPosterGenerator;
import com.won.smarketing.content.presentation.dto.PosterContentCreateRequest;
import com.won.smarketing.content.presentation.dto.PosterContentCreateResponse;
import com.won.smarketing.content.presentation.dto.PosterContentSaveRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.Map;

/**
 * 포스터 콘텐츠 서비스 구현체
 * 홍보 포스터 생성 및 저장 기능 구현
 */
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class PosterContentService implements PosterContentUseCase {

    private final ContentRepository contentRepository;
    private final AiPosterGenerator aiPosterGenerator;

    /**
     * 포스터 콘텐츠 생성
     * 
     * @param request 포스터 콘텐츠 생성 요청
     * @return 생성된 포스터 콘텐츠 정보
     */
    @Override
    @Transactional
    public PosterContentCreateResponse generatePosterContent(PosterContentCreateRequest request) {
        // AI를 사용하여 포스터 생성
        String generatedPoster = aiPosterGenerator.generatePoster(request);
        
        // 다양한 사이즈의 포스터 생성
        Map<String, String> posterSizes = aiPosterGenerator.generatePosterSizes(generatedPoster);

        // 생성 조건 정보 구성
        CreationConditions conditions = CreationConditions.builder()
                .category(request.getCategory())
                .requirement(request.getRequirement())
                .toneAndManner(request.getToneAndManner())
                .emotionIntensity(request.getEmotionIntensity())
                .eventName(request.getEventName())
                .startDate(request.getStartDate())
                .endDate(request.getEndDate())
                .photoStyle(request.getPhotoStyle())
                .build();

        return PosterContentCreateResponse.builder()
                .contentId(null) // 임시 생성이므로 ID 없음
                .contentType(ContentType.POSTER.name())
                .title(request.getTitle())
                .posterImage(generatedPoster)
                .posterSizes(posterSizes)
                .status(ContentStatus.DRAFT.name())
                //.createdAt(LocalDateTime.now())
                .build();
    }

    /**
     * 포스터 콘텐츠 저장
     * 
     * @param request 포스터 콘텐츠 저장 요청
     */
    @Override
    @Transactional
    public void savePosterContent(PosterContentSaveRequest request) {
        // 생성 조건 정보 구성
        CreationConditions conditions = CreationConditions.builder()
                .category(request.getCategory())
                .requirement(request.getRequirement())
                .toneAndManner(request.getToneAndManner())
                .emotionIntensity(request.getEmotionIntensity())
                .eventName(request.getEventName())
                .startDate(request.getStartDate())
                .endDate(request.getEndDate())
                .photoStyle(request.getPhotoStyle())
                .build();

        // 콘텐츠 엔티티 생성 및 저장
        Content content = Content.builder()
                .contentType(ContentType.POSTER)
                .platform(Platform.GENERAL) // 포스터는 범용
                .title(request.getTitle())
                .content(null) // 포스터는 이미지가 주 콘텐츠
                .hashtags(null)
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
