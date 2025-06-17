package com.won.smarketing.content.domain.service;

import com.won.smarketing.content.presentation.dto.PosterContentCreateRequest;

import java.util.Map;

/**
 * AI 포스터 생성 도메인 서비스 인터페이스
 * 홍보 포스터 생성 및 다양한 사이즈 생성 기능 정의
 */
public interface AiPosterGenerator {
    
    /**
     * 포스터 생성
     * 
     * @param request 포스터 생성 요청
     * @return 생성된 포스터 이미지 URL
     */
    String generatePoster(PosterContentCreateRequest request);
}
