package com.won.smarketing.content.domain.service;

import com.won.smarketing.content.domain.model.Platform;
import com.won.smarketing.content.presentation.dto.SnsContentCreateRequest;
import com.won.smarketing.content.presentation.dto.SnsContentCreateResponse;

import java.util.List;

/**
 * AI 콘텐츠 생성 도메인 서비스 인터페이스
 * SNS 콘텐츠 생성 및 해시태그 생성 기능 정의
 */
public interface AiContentGenerator {
    
    /**
     * SNS 콘텐츠 생성
     * 
     * @param request SNS 콘텐츠 생성 요청
     * @return 생성된 콘텐츠
     */
    String generateSnsContent(SnsContentCreateRequest request);
}
