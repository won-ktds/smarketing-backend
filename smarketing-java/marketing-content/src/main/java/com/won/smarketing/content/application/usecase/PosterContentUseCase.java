// marketing-content/src/main/java/com/won/smarketing/content/application/usecase/PosterContentUseCase.java
package com.won.smarketing.content.application.usecase;

import com.won.smarketing.content.domain.model.Content;
import com.won.smarketing.content.presentation.dto.PosterContentCreateRequest;
import com.won.smarketing.content.presentation.dto.PosterContentCreateResponse;
import com.won.smarketing.content.presentation.dto.PosterContentSaveRequest;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

/**
 * 포스터 콘텐츠 관련 UseCase 인터페이스
 * Clean Architecture의 Application Layer에서 비즈니스 로직 정의
 */
public interface PosterContentUseCase {

    /**
     * 포스터 콘텐츠 생성
     * @param request 포스터 콘텐츠 생성 요청
     * @return 포스터 콘텐츠 생성 응답
     */
    PosterContentCreateResponse generatePosterContent(List<MultipartFile> images, PosterContentCreateRequest request);

    /**
     * 포스터 콘텐츠 저장
     * @param request 포스터 콘텐츠 저장 요청
     */
    Content savePosterContent(PosterContentSaveRequest request);
}