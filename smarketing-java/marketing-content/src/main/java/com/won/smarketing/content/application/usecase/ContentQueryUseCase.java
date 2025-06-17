package com.won.smarketing.content.application.usecase;

import com.won.smarketing.content.presentation.dto.*;

import java.util.List;

/**
 * 콘텐츠 조회 관련 Use Case 인터페이스
 * 콘텐츠 수정, 조회, 삭제 기능 정의
 */
public interface ContentQueryUseCase {
    
    /**
     * 콘텐츠 수정
     * 
     * @param contentId 수정할 콘텐츠 ID
     * @param request 콘텐츠 수정 요청
     * @return 수정된 콘텐츠 정보
     */
    ContentUpdateResponse updateContent(Long contentId, ContentUpdateRequest request);
    
    /**
     * 콘텐츠 목록 조회
     * 
     * @param storeId 콘텐츠 타입
     * @param platform 플랫폼

     * @return 콘텐츠 목록
     */
    List<ContentResponse> getContents(Long storeId, String platform);
    
    /**
     * 진행 중인 콘텐츠 목록 조회
     * 
     * @param period 기간
     * @return 진행 중인 콘텐츠 목록
     */
    List<OngoingContentResponse> getOngoingContents(String period);
    
    /**
     * 콘텐츠 상세 조회
     * 
     * @param contentId 콘텐츠 ID
     * @return 콘텐츠 상세 정보
     */
    //ContentDetailResponse getContentDetail(Long contentId);
    
    /**
     * 콘텐츠 삭제
     * 
     * @param contentId 삭제할 콘텐츠 ID
     */
    void deleteContent(Long contentId);
}
