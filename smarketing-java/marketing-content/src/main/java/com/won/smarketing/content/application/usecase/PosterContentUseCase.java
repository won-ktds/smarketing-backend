package com.won.smarketing.content.application.usecase;

import com.won.smarketing.content.presentation.dto.PosterContentCreateRequest;
import com.won.smarketing.content.presentation.dto.PosterContentCreateResponse;
import com.won.smarketing.content.presentation.dto.PosterContentSaveRequest;

/**
 * 포스터 콘텐츠 관련 Use Case 인터페이스
 * 홍보 포스터 생성 및 저장 기능 정의
 */
public interface PosterContentUseCase {
    
    /**
     * 포스터 콘텐츠 생성
     * 
     * @param request 포스터 콘텐츠 생성 요청
     * @return 생성된 포스터 콘텐츠 정보
     */
    PosterContentCreateResponse generatePosterContent(PosterContentCreateRequest request);
    
    /**
     * 포스터 콘텐츠 저장
     * 
     * @param request 포스터 콘텐츠 저장 요청
     */
    void savePosterContent(PosterContentSaveRequest request);
}
