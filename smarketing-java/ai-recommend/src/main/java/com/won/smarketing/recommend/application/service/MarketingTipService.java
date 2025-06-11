package com.won.smarketing.recommend.application.service;

import com.won.smarketing.common.exception.BusinessException;
import com.won.smarketing.common.exception.ErrorCode;
import com.won.smarketing.recommend.application.usecase.MarketingTipUseCase;
import com.won.smarketing.recommend.domain.model.MarketingTip;
import com.won.smarketing.recommend.domain.model.StoreData;
import com.won.smarketing.recommend.domain.model.TipId;
import com.won.smarketing.recommend.domain.model.WeatherData;
import com.won.smarketing.recommend.domain.repository.MarketingTipRepository;
import com.won.smarketing.recommend.domain.service.StoreDataProvider;
import com.won.smarketing.recommend.domain.service.WeatherDataProvider;
import com.won.smarketing.recommend.domain.service.AiTipGenerator;
import com.won.smarketing.recommend.presentation.dto.MarketingTipRequest;
import com.won.smarketing.recommend.presentation.dto.MarketingTipResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 마케팅 팁 서비스 구현체
 */
@Slf4j
@Service
@RequiredArgsConstructor
@Transactional
public class MarketingTipService implements MarketingTipUseCase {

    private final MarketingTipRepository marketingTipRepository;
    private final StoreDataProvider storeDataProvider;
    private final WeatherDataProvider weatherDataProvider;
    private final AiTipGenerator aiTipGenerator;

    @Override
    public MarketingTipResponse generateMarketingTips(MarketingTipRequest request) {
        log.info("마케팅 팁 생성 시작: storeId={}", request.getStoreId());

        try {
            // 1. 매장 정보 조회
            StoreData storeData = storeDataProvider.getStoreData(request.getStoreId());
            log.debug("매장 정보 조회 완료: {}", storeData.getStoreName());

            // 2. 날씨 정보 조회
            WeatherData weatherData = weatherDataProvider.getCurrentWeather(storeData.getLocation());
            log.debug("날씨 정보 조회 완료: 온도={}, 상태={}", weatherData.getTemperature(), weatherData.getCondition());

            // 3. AI 팁 생성
            String aiGeneratedTip = aiTipGenerator.generateTip(storeData, weatherData, request.getAdditionalRequirement());
            log.debug("AI 팁 생성 완료: {}", aiGeneratedTip.substring(0, Math.min(50, aiGeneratedTip.length())));

            // 4. 도메인 객체 생성 및 저장
            MarketingTip marketingTip = MarketingTip.builder()
                    .storeId(request.getStoreId())
                    .tipContent(aiGeneratedTip)
                    .weatherData(weatherData)
                    .storeData(storeData)
                    .build();

            MarketingTip savedTip = marketingTipRepository.save(marketingTip);
            log.info("마케팅 팁 저장 완료: tipId={}", savedTip.getId().getValue());

            return convertToResponse(savedTip);

        } catch (Exception e) {
            log.error("마케팅 팁 생성 중 오류: storeId={}", request.getStoreId(), e);
            throw new BusinessException(ErrorCode.AI_TIP_GENERATION_FAILED);
        }
    }

    @Override
    @Transactional(readOnly = true)
    @Cacheable(value = "marketingTipHistory", key = "#storeId + '_' + #pageable.pageNumber + '_' + #pageable.pageSize")
    public Page<MarketingTipResponse> getMarketingTipHistory(Long storeId, Pageable pageable) {
        log.info("마케팅 팁 이력 조회: storeId={}", storeId);

        Page<MarketingTip> tips = marketingTipRepository.findByStoreIdOrderByCreatedAtDesc(storeId, pageable);

        return tips.map(this::convertToResponse);
    }

    @Override
    @Transactional(readOnly = true)
    public MarketingTipResponse getMarketingTip(Long tipId) {
        log.info("마케팅 팁 상세 조회: tipId={}", tipId);

        MarketingTip marketingTip = marketingTipRepository.findById(tipId)
                .orElseThrow(() -> new BusinessException(ErrorCode.MARKETING_TIP_NOT_FOUND));

        return convertToResponse(marketingTip);
    }

    private MarketingTipResponse convertToResponse(MarketingTip marketingTip) {
        return MarketingTipResponse.builder()
                .tipId(marketingTip.getId().getValue())
                .storeId(marketingTip.getStoreId())
                .storeName(marketingTip.getStoreData().getStoreName())
                .businessType(marketingTip.getStoreData().getBusinessType())
                .storeLocation(marketingTip.getStoreData().getLocation())
                .createdAt(marketingTip.getCreatedAt())
                .build();
    }

    public MarketingTip toDomain() {
        WeatherData weatherData = WeatherData.builder()
                .temperature(this.weatherTemperature)
                .condition(this.weatherCondition)
                .humidity(this.weatherHumidity)
                .build();

        StoreData storeData = StoreData.builder()
                .storeName(this.storeName)
                .businessType(this.businessType)
                .location(this.storeLocation)
                .build();

        return MarketingTip.builder()
                .id(this.id != null ? TipId.of(this.id) : null)
                .storeId(this.storeId)
                .tipContent(this.tipContent)
                .weatherData(weatherData)
                .storeData(storeData)
                .createdAt(this.createdAt)
                .build();
    }
}