package com.won.smarketing.recommend.application.usecase;

import com.won.smarketing.recommend.presentation.dto.MarketingTipRequest;
import com.won.smarketing.recommend.presentation.dto.MarketingTipResponse;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

/**
 * 마케팅 팁 유즈케이스 인터페이스
 */
public interface MarketingTipUseCase {
    
    /**
     * AI 마케팅 팁 생성
     */
    MarketingTipResponse generateMarketingTips(MarketingTipRequest request);
    
    /**
     * 마케팅 팁 이력 조회
     */
    Page<MarketingTipResponse> getMarketingTipHistory(Long storeId, Pageable pageable);
    
    /**
     * 마케팅 팁 상세 조회
     */
    MarketingTipResponse getMarketingTip(Long tipId);
}
