package com.won.smarketing.recommend.application.usecase;

import com.won.smarketing.recommend.presentation.dto.MarketingTipResponse;

public interface MarketingTipUseCase {

    /**
     * 마케팅 팁 제공
     * 1시간 이내 팁이 있으면 기존 것 사용, 없으면 새로 생성
     */
    MarketingTipResponse provideMarketingTip();
}