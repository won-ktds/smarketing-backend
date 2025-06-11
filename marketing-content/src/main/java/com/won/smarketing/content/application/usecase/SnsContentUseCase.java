package com.won.smarketing.content.application.usecase;

import com.won.smarketing.content.presentation.dto.SnsContentCreateRequest;
import com.won.smarketing.content.presentation.dto.SnsContentCreateResponse;
import com.won.smarketing.content.presentation.dto.SnsContentSaveRequest;

/**
 * SNS 콘텐츠 관련 Use Case 인터페이스
 * SNS 게시물 생성 및 저장 기능 정의
 */
public interface SnsContentUseCase {
    
    /**
     * SNS 콘텐츠 생성
     * 
     * @param request SNS 콘텐츠 생성 요청
     * @return 생성된 SNS 콘텐츠 정보
     */
    SnsContentCreateResponse generateSnsContent(SnsContentCreateRequest request);
    
    /**
     * SNS 콘텐츠 저장
     * 
     * @param request SNS 콘텐츠 저장 요청
     */
    void saveSnsContent(SnsContentSaveRequest request);
}
