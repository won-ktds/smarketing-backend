package com.won.smarketing.recommend.application.service;

import com.won.smarketing.common.exception.BusinessException;
import com.won.smarketing.common.exception.ErrorCode;
import com.won.smarketing.recommend.application.usecase.MarketingTipUseCase;
import com.won.smarketing.recommend.domain.model.MarketingTip;
import com.won.smarketing.recommend.domain.model.StoreData;
import com.won.smarketing.recommend.domain.model.TipId;
import com.won.smarketing.recommend.domain.model.WeatherData;
import com.won.smarketing.recommend.domain.repository.MarketingTipRepository;
import com.won.smarketing.recommend.domain.service.AiTipGenerator;
import com.won.smarketing.recommend.domain.service.StoreDataProvider;
import com.won.smarketing.recommend.domain.service.WeatherDataProvider;
import com.won.smarketing.recommend.presentation.dto.MarketingTipRequest;
import com.won.smarketing.recommend.presentation.dto.MarketingTipResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;

/**
 * 마케팅 팁 서비스 구현체
 * AI 기반 마케팅 팁 생성 및 저장 기능 구현
 */
@Slf4j
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class MarketingTipService implements MarketingTipUseCase {

    private final MarketingTipRepository marketingTipRepository;
    private final StoreDataProvider storeDataProvider;
    private final WeatherDataProvider weatherDataProvider;
    private final AiTipGenerator aiTipGenerator;

    /**
     * AI 마케팅 팁 생성
     * 
     * @param request 마케팅 팁 생성 요청
     * @return 생성된 마케팅 팁 응답
     */
    @Override
    @Transactional
    public MarketingTipResponse generateMarketingTips(MarketingTipRequest request) {
        try {
            // 매장 정보 조회
            StoreData storeData = storeDataProvider.getStoreData(request.getStoreId());
            log.debug("매장 정보 조회 완료: {}", storeData.getStoreName());

            // 날씨 정보 조회
            WeatherData weatherData = weatherDataProvider.getCurrentWeather(storeData.getLocation());
            log.debug("날씨 정보 조회 완료: {} 도", weatherData.getTemperature());

            // AI를 사용하여 마케팅 팁 생성
            String tipContent = aiTipGenerator.generateTip(storeData, weatherData);
            log.debug("AI 마케팅 팁 생성 완료");

            // 마케팅 팁 도메인 객체 생성
            MarketingTip marketingTip = MarketingTip.builder()
                    .storeId(request.getStoreId())
                    .tipContent(tipContent)
                    .weatherData(weatherData)
                    .storeData(storeData)
                    .createdAt(LocalDateTime.now())
                    .build();

            // 마케팅 팁 저장
            MarketingTip savedTip = marketingTipRepository.save(marketingTip);

            return MarketingTipResponse.builder()
                    .tipId(savedTip.getId().getValue())
                    .tipContent(savedTip.getTipContent())
                    .createdAt(savedTip.getCreatedAt())
                    .build();

        } catch (Exception e) {
            log.error("마케팅 팁 생성 중 오류 발생", e);
            throw new BusinessException(ErrorCode.RECOMMENDATION_FAILED);
        }
    }
}
