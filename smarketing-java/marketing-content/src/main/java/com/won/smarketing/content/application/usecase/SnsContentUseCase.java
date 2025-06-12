// marketing-content/src/main/java/com/won/smarketing/content/application/usecase/SnsContentUseCase.java
package com.won.smarketing.content.application.usecase;

import com.won.smarketing.content.presentation.dto.SnsContentCreateRequest;
import com.won.smarketing.content.presentation.dto.SnsContentCreateResponse;
import com.won.smarketing.content.presentation.dto.SnsContentSaveRequest;

/**
 * SNS 콘텐츠 관련 UseCase 인터페이스
 * Clean Architecture의 Application Layer에서 비즈니스 로직 정의
 */
public interface SnsContentUseCase {

    /**
     * SNS 콘텐츠 생성
     * @param request SNS 콘텐츠 생성 요청
     * @return SNS 콘텐츠 생성 응답
     */
    SnsContentCreateResponse generateSnsContent(SnsContentCreateRequest request);

    /**
     * SNS 콘텐츠 저장
     * @param request SNS 콘텐츠 저장 요청
     */
    void saveSnsContent(SnsContentSaveRequest request);
}