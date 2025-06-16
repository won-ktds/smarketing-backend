package com.won.smarketing.recommend.application.service;

import com.won.smarketing.common.exception.BusinessException;
import com.won.smarketing.common.exception.ErrorCode;
import com.won.smarketing.recommend.application.usecase.MarketingTipUseCase;
import com.won.smarketing.recommend.domain.model.MarketingTip;
import com.won.smarketing.recommend.domain.model.StoreData;
import com.won.smarketing.recommend.domain.repository.MarketingTipRepository;
import com.won.smarketing.recommend.domain.service.AiTipGenerator;
import com.won.smarketing.recommend.domain.service.StoreDataProvider;
import com.won.smarketing.recommend.presentation.dto.MarketingTipResponse;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Optional;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional
public class MarketingTipService implements MarketingTipUseCase {

    private final MarketingTipRepository marketingTipRepository;
    private final StoreDataProvider storeDataProvider;
    private final AiTipGenerator aiTipGenerator;

    @Override
    public MarketingTipResponse provideMarketingTip() {
        String userId = getCurrentUserId();
        log.info("마케팅 팁 제공: userId={}", userId);

        try {
            // 1. 사용자의 매장 정보 조회
            StoreData storeData = storeDataProvider.getStoreDataByUserId(userId);

            // 2. 1시간 이내에 생성된 마케팅 팁이 있는지 DB에서 확인
            Optional<MarketingTip> recentTip = findRecentMarketingTip(storeData.getStoreId());

            if (recentTip.isPresent()) {
                log.info("1시간 이내에 생성된 마케팅 팁 발견: tipId={}", recentTip.get().getId().getValue());
                log.info("1시간 이내에 생성된 마케팅 팁 발견: getTipContent()={}", recentTip.get().getTipContent());
                return convertToResponse(recentTip.get(), storeData, true);
            }

            // 3. 1시간 이내 팁이 없으면 새로 생성
            log.info("1시간 이내 마케팅 팁이 없어 새로 생성합니다: userId={}, storeId={}", userId, storeData.getStoreId());
            MarketingTip newTip = createNewMarketingTip(storeData);
            return convertToResponse(newTip, storeData, false);

        } catch (Exception e) {
            log.error("마케팅 팁 조회/생성 중 오류: userId={}", userId, e);
            throw new BusinessException(ErrorCode.INTERNAL_SERVER_ERROR);
        }
    }

    /**
     * DB에서 1시간 이내 생성된 마케팅 팁 조회
     */
    private Optional<MarketingTip> findRecentMarketingTip(Long storeId) {
        log.debug("DB에서 1시간 이내 마케팅 팁 조회: storeId={}", storeId);

        // 최근 생성된 팁 1개 조회
        Pageable pageable = PageRequest.of(0, 1);
        Page<MarketingTip> recentTips = marketingTipRepository.findByStoreIdOrderByCreatedAtDesc(storeId, pageable);

        if (recentTips.isEmpty()) {
            log.debug("매장의 마케팅 팁이 존재하지 않음: storeId={}", storeId);
            return Optional.empty();
        }

        MarketingTip mostRecentTip = recentTips.getContent().get(0);
        LocalDateTime oneHourAgo = LocalDateTime.now().minusHours(1);

        // 1시간 이내에 생성된 팁인지 확인
        if (mostRecentTip.getCreatedAt().isAfter(oneHourAgo)) {
            log.debug("1시간 이내 마케팅 팁 발견: tipId={}, 생성시간={}",
                    mostRecentTip.getId().getValue(), mostRecentTip.getCreatedAt());
            return Optional.of(mostRecentTip);
        }

        log.debug("가장 최근 팁이 1시간 이전에 생성됨: tipId={}, 생성시간={}",
                mostRecentTip.getId().getValue(), mostRecentTip.getCreatedAt());
        return Optional.empty();
    }

    /**
     * 새로운 마케팅 팁 생성
     */
    private MarketingTip createNewMarketingTip(StoreData storeData) {
        log.info("새로운 마케팅 팁 생성 시작: storeName={}", storeData.getStoreName());

        // AI 서비스로 팁 생성
        String aiGeneratedTip = aiTipGenerator.generateTip(storeData);
        log.debug("AI 팁 생성 완료: {}", aiGeneratedTip.substring(0, Math.min(50, aiGeneratedTip.length())));

        // 도메인 객체 생성 및 저장
        MarketingTip marketingTip = MarketingTip.builder()
                .storeId(storeData.getStoreId())
                .tipContent(aiGeneratedTip)
                .storeData(storeData)
                .createdAt(LocalDateTime.now())
                .build();

        MarketingTip savedTip = marketingTipRepository.save(marketingTip);
        log.info("새로운 마케팅 팁 저장 완료: tipId={}", savedTip.getId().getValue());
        log.info("새로운 마케팅 팁 저장 완료: savedTip.getTipContent()={}", savedTip.getTipContent());

        return savedTip;
    }

    /**
     * 마케팅 팁을 응답 DTO로 변환 (전체 내용 포함)
     */
    private MarketingTipResponse convertToResponse(MarketingTip marketingTip, StoreData storeData, boolean isRecentlyCreated) {
        String tipSummary = generateTipSummary(marketingTip.getTipContent());

        return MarketingTipResponse.builder()
                .tipId(marketingTip.getId().getValue())
                .tipSummary(tipSummary)
                .tipContent(marketingTip.getTipContent())  // 🆕 전체 내용 포함
                .storeInfo(MarketingTipResponse.StoreInfo.builder()
                        .storeName(storeData.getStoreName())
                        .businessType(storeData.getBusinessType())
                        .location(storeData.getLocation())
                        .build())
                .createdAt(marketingTip.getCreatedAt())
                .updatedAt(marketingTip.getUpdatedAt())
                .isRecentlyCreated(isRecentlyCreated)
                .build();
    }

    /**
     * 마케팅 팁 요약 생성 (첫 50자 또는 첫 번째 문장)
     */
    private String generateTipSummary(String fullContent) {
        if (fullContent == null || fullContent.trim().isEmpty()) {
            return "마케팅 팁이 생성되었습니다.";
        }

        // 첫 번째 문장으로 요약 (마침표 기준)
        String[] sentences = fullContent.split("[.!?]");
        String firstSentence = sentences.length > 0 ? sentences[0].trim() : fullContent;

        // 50자 제한
        if (firstSentence.length() > 50) {
            return firstSentence.substring(0, 47) + "...";
        }

        return firstSentence;
    }

    /**
     * 현재 로그인된 사용자 ID 조회
     */
    private String getCurrentUserId() {
        return SecurityContextHolder.getContext().getAuthentication().getName();
    }
}