package com.won.smarketing.recommend.application.usecase;

import com.won.smarketing.recommend.presentation.dto.MarketingTipRequest;
import com.won.smarketing.recommend.presentation.dto.MarketingTipResponse;

/**
 * 마케팅 팁 관련 Use Case 인터페이스
 * AI 기반 마케팅 팁 생성 기능 정의
 */
public interface MarketingTipUseCase {
    
    /**
     * AI 마케팅 팁 생성
     * 
     * @param request 마케팅 팁 생성 요청
     * @return 생성된 마케팅 팁 응답
     */
    MarketingTipResponse generateMarketingTips(MarketingTipRequest request);
}
