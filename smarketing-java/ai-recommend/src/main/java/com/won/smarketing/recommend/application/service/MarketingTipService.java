package com.won.smarketing.recommend.application.service;

import com.won.smarketing.common.exception.BusinessException;
import com.won.smarketing.common.exception.ErrorCode;
import com.won.smarketing.recommend.application.usecase.MarketingTipUseCase;
import com.won.smarketing.recommend.domain.model.MarketingTip;
import com.won.smarketing.recommend.domain.model.MenuData;
import com.won.smarketing.recommend.domain.model.StoreData;
import com.won.smarketing.recommend.domain.model.StoreWithMenuData;
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
import java.util.List;
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
            StoreWithMenuData storeWithMenuData = storeDataProvider.getStoreWithMenuData(userId);

            // 2. 1시간 이내에 생성된 마케팅 팁이 있는지 DB에서 확인
            Optional<MarketingTip> recentTip = findRecentMarketingTip(storeWithMenuData.getStoreData().getStoreId());

            if (recentTip.isPresent()) {
                log.info("1시간 이내에 생성된 마케팅 팁 발견: tipId={}", recentTip.get().getId().getValue());
                log.info("1시간 이내에 생성된 마케팅 팁 발견: getTipContent()={}", recentTip.get().getTipContent());
                return convertToResponse(recentTip.get(), storeWithMenuData.getStoreData(), true);
            }

            // 3. 1시간 이내 팁이 없으면 새로 생성
            log.info("1시간 이내 마케팅 팁이 없어 새로 생성합니다: userId={}, storeId={}", userId, storeWithMenuData.getStoreData().getStoreId());
            MarketingTip newTip = createNewMarketingTip(storeWithMenuData);
            return convertToResponse(newTip, storeWithMenuData.getStoreData(), false);

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
    private MarketingTip createNewMarketingTip(StoreWithMenuData storeWithMenuData) {
        log.info("새로운 마케팅 팁 생성 시작: storeName={}", storeWithMenuData.getStoreData().getStoreName());

        // AI 서비스로 팁 생성
        String aiGeneratedTip = aiTipGenerator.generateTip(storeWithMenuData);
        log.debug("AI 팁 생성 완료: {}", aiGeneratedTip.substring(0, Math.min(50, aiGeneratedTip.length())));

        String tipSummary = generateTipSummary(aiGeneratedTip);

        // 도메인 객체 생성 및 저장
        MarketingTip marketingTip = MarketingTip.builder()
                .storeId(storeWithMenuData.getStoreData().getStoreId())
                .tipSummary(tipSummary)
                .tipContent(aiGeneratedTip)
                .storeWithMenuData(storeWithMenuData)
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

        return MarketingTipResponse.builder()
                .tipId(marketingTip.getId().getValue())
                .tipSummary(marketingTip.getTipSummary())
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
     * 마케팅 팁 요약 생성 (핵심 마케팅 팁 섹션에서 첫 번째 문장 추출)
     *
     * @param fullContent AI로 생성된 전체 마케팅 팁 HTML 콘텐츠
     * @return 핵심 마케팅 팁의 첫 번째 문장
     */
    private String generateTipSummary(String fullContent) {
        if (fullContent == null || fullContent.trim().isEmpty()) {
            return "마케팅 팁이 생성되었습니다.";
        }

        try {
            // 1. "✨ 핵심 마케팅 팁" 섹션 추출
            String coreSection = extractCoreMarketingTipSection(fullContent);

            if (coreSection != null && !coreSection.trim().isEmpty()) {
                // 2. HTML 태그 제거
                String cleanText = removeHtmlTags(coreSection);

                // 3. 첫 번째 의미있는 문장 추출
                String summary = extractFirstMeaningfulSentence(cleanText);

                // 4. 길이 제한 (100자 이내)
                if (summary.length() > 100) {
                    summary = summary.substring(0, 97) + "...";
                }

                return summary;
            }

            // 핵심 팁 섹션을 찾지 못한 경우 fallback 처리
            return extractFallbackSummary(fullContent);

        } catch (Exception e) {
            log.warn("마케팅 팁 요약 생성 중 오류 발생, 기본 메시지 반환: {}", e.getMessage());
            return "맞춤형 마케팅 팁이 생성되었습니다.";
        }
    }

    /**
     * "✨ 핵심 마케팅 팁" 섹션 추출
     */
    private String extractCoreMarketingTipSection(String fullContent) {
        // 핵심 마케팅 팁 섹션 시작 패턴들
        String[] corePatterns = {
                "✨ 핵심 마케팅 팁",
                "<h3>✨ 핵심 마케팅 팁</h3>",
                "핵심 마케팅 팁"
        };

        // 다음 섹션 시작 패턴들
        String[] nextSectionPatterns = {
                "🚀 실행 방법",
                "<h3>🚀 실행 방법</h3>",
                "💰 예상 비용",
                "<h3>💰 예상 비용"
        };

        for (String pattern : corePatterns) {
            int startIndex = fullContent.indexOf(pattern);
            if (startIndex != -1) {
                // 패턴 뒤부터 시작
                int contentStart = startIndex + pattern.length();

                // 다음 섹션까지의 내용 추출
                int endIndex = fullContent.length();
                for (String nextPattern : nextSectionPatterns) {
                    int nextIndex = fullContent.indexOf(nextPattern, contentStart);
                    if (nextIndex != -1 && nextIndex < endIndex) {
                        endIndex = nextIndex;
                    }
                }

                return fullContent.substring(contentStart, endIndex).trim();
            }
        }

        return null;
    }

    /**
     * HTML 태그 제거
     */
    private String removeHtmlTags(String htmlText) {
        if (htmlText == null) return "";

        return htmlText
                .replaceAll("<[^>]+>", "")  // HTML 태그 제거
                .replaceAll("&nbsp;", " ")  // HTML 엔티티 처리
                .replaceAll("&lt;", "<")
                .replaceAll("&gt;", ">")
                .replaceAll("&amp;", "&")
                .replaceAll("\\s+", " ")    // 연속된 공백을 하나로
                .trim();
    }

    /**
     * 첫 번째 의미있는 문장 추출
     */
    private String extractFirstMeaningfulSentence(String cleanText) {
        if (cleanText == null || cleanText.trim().isEmpty()) {
            return "마케팅 팁이 생성되었습니다.";
        }

        // 문장 분할 (마침표, 느낌표, 물음표 기준)
        String[] sentences = cleanText.split("[.!?]");

        for (String sentence : sentences) {
            String trimmed = sentence.trim();

            // 의미있는 문장인지 확인 (10자 이상, 특수문자만으로 구성되지 않음)
            if (trimmed.length() >= 10 &&
                    !trimmed.matches("^[\\s\\p{Punct}]*$") &&  // 공백과 구두점만으로 구성되지 않음
                    !isOnlyEmojisOrSymbols(trimmed)) {         // 이모지나 기호만으로 구성되지 않음

                // 문장 끝에 마침표 추가 (없는 경우)
                if (!trimmed.endsWith(".") && !trimmed.endsWith("!") && !trimmed.endsWith("?")) {
                    trimmed += ".";
                }

                return trimmed;
            }
        }

        // 의미있는 문장을 찾지 못한 경우 원본의 처음 50자 반환
        if (cleanText.length() > 50) {
            return cleanText.substring(0, 47) + "...";
        }

        return cleanText;
    }

    /**
     * 이모지나 기호만으로 구성되었는지 확인
     */
    private boolean isOnlyEmojisOrSymbols(String text) {
        // 한글, 영문, 숫자가 포함되어 있으면 의미있는 텍스트로 판단
        return !text.matches(".*[\\p{L}\\p{N}].*");
    }

    /**
     * 핵심 팁 섹션을 찾지 못한 경우 대체 요약 생성
     */
    private String extractFallbackSummary(String fullContent) {
        // HTML 태그 제거 후 첫 번째 의미있는 문장 찾기
        String cleanContent = removeHtmlTags(fullContent);

        // 첫 번째 문단에서 의미있는 문장 추출
        String[] paragraphs = cleanContent.split("\\n\\n");

        for (String paragraph : paragraphs) {
            String trimmed = paragraph.trim();
            if (trimmed.length() >= 20) {  // 충분히 긴 문단
                String summary = extractFirstMeaningfulSentence(trimmed);
                if (summary.length() >= 10) {
                    return summary;
                }
            }
        }

        // 모든 방법이 실패한 경우 기본 메시지
        return "개인화된 마케팅 팁이 생성되었습니다.";
    }

    /**
     * 현재 로그인된 사용자 ID 조회
     */
    private String getCurrentUserId() {
        return SecurityContextHolder.getContext().getAuthentication().getName();
    }
}