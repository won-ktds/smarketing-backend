package com.won.smarketing.content.application.service;

import com.won.smarketing.content.application.usecase.PosterContentUseCase;
import com.won.smarketing.content.domain.model.Content;
import com.won.smarketing.content.domain.model.ContentStatus;
import com.won.smarketing.content.domain.model.ContentType;
import com.won.smarketing.content.domain.model.CreationConditions;
import com.won.smarketing.content.domain.model.Platform;
import com.won.smarketing.content.domain.repository.ContentRepository;
import com.won.smarketing.content.domain.service.AiPosterGenerator;
import com.won.smarketing.content.domain.service.BlobStorageService;
import com.won.smarketing.content.presentation.dto.PosterContentCreateRequest;
import com.won.smarketing.content.presentation.dto.PosterContentCreateResponse;
import com.won.smarketing.content.presentation.dto.PosterContentSaveRequest;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

/**
 * 포스터 콘텐츠 서비스 구현체
 * 홍보 포스터 생성 및 저장 기능 구현
 */
@Service
@Slf4j
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class PosterContentService implements PosterContentUseCase {

    @Value("${azure.storage.container.poster-images:poster-images}")
    private String posterImageContainer;

    private final ContentRepository contentRepository;
    private final AiPosterGenerator aiPosterGenerator;
    private final BlobStorageService blobStorageService;

    /**
     * 포스터 콘텐츠 생성
     *
     * @param request 포스터 콘텐츠 생성 요청
     * @return 생성된 포스터 콘텐츠 정보
     */
    @Override
    @Transactional
    public PosterContentCreateResponse generatePosterContent(List<MultipartFile> images, PosterContentCreateRequest request) {

        // 1. 이미지 blob storage에 저장하고 request 저장
        List<String> imageUrls = blobStorageService.uploadImage(images, posterImageContainer);
        request.setImages(imageUrls);

        // 2. AI 요청
        String generatedPoster = aiPosterGenerator.generatePoster(request);

        return PosterContentCreateResponse.builder()
                .contentId(null) // 임시 생성이므로 ID 없음
                .contentType(ContentType.POSTER.name())
                .title(request.getTitle())
                .content(generatedPoster)
                .status(ContentStatus.DRAFT.name())
                .build();
    }

    /**
     * 포스터 콘텐츠 저장
     *
     * @param request 포스터 콘텐츠 저장 요청
     */
    @Transactional
    public void savePosterContent(PosterContentSaveRequest request) {
        // 생성 조건 구성
        CreationConditions conditions = CreationConditions.builder()
                .category(request.getCategory())
                .requirement(request.getRequirement())
                .eventName(request.getEventName())
                .startDate(request.getStartDate())
                .endDate(request.getEndDate())
                .photoStyle(request.getPhotoStyle())
                .build();

        // 콘텐츠 엔티티 생성
        Content content = Content.builder()
                .contentType(ContentType.POSTER)
                .platform(Platform.GENERAL)
                .title(request.getTitle())
                .content(request.getContent())
                .images(request.getImages())
                .status(ContentStatus.PUBLISHED)
                .creationConditions(conditions)
                .storeId(request.getStoreId())
                .build();

        // 저장
        contentRepository.save(content);
    }
}