package com.won.smarketing.recommend.application.usecase;

import com.won.smarketing.recommend.presentation.dto.MarketingTipRequest;
import com.won.smarketing.recommend.presentation.dto.MarketingTipResponse;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

/**
 * 마케팅 팁 생성 유즈케이스 인터페이스
 * 비즈니스 요구사항을 정의하는 애플리케이션 계층의 인터페이스
 */
public interface MarketingTipUseCase {

    /**
     * AI 마케팅 팁 생성
     *
     * @param request 마케팅 팁 생성 요청
     * @return 생성된 마케팅 팁 정보
     */
    MarketingTipResponse generateMarketingTips(MarketingTipRequest request);

    /**
     * 마케팅 팁 이력 조회
     *
     * @param storeId 매장 ID
     * @param pageable 페이징 정보
     * @return 마케팅 팁 이력 페이지
     */
    Page<MarketingTipResponse> getMarketingTipHistory(Long storeId, Pageable pageable);

    /**
     * 마케팅 팁 상세 조회
     *
     * @param tipId 팁 ID
     * @return 마케팅 팁 상세 정보
     */
    MarketingTipResponse getMarketingTip(Long tipId);
}