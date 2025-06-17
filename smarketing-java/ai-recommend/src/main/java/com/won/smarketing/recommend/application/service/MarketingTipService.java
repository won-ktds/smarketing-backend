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
        log.info("tipSummary : {}", tipSummary);

        // 도메인 객체 생성 및 저장
        MarketingTip marketingTip = MarketingTip.builder()
                .storeId(storeWithMenuData.getStoreData().getStoreId())
                .tipContent(aiGeneratedTip)
                .tipSummary(tipSummary)
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

    private String generateTipSummary(String fullContent) {
        if (fullContent == null || fullContent.trim().isEmpty()) {
            return "마케팅 팁이 생성되었습니다.";
        }

        try {
            // JSON 형식 처리: "```html\n..." 패턴
            String processedContent = preprocessContent(fullContent);

            // 1순위: HTML 블록 밖의 첫 번째 제목 추출
            String titleOutsideHtml = extractTitleOutsideHtml(processedContent);
            if (titleOutsideHtml != null && titleOutsideHtml.length() > 5) {
                return titleOutsideHtml;
            }

            // 2순위: <b> 태그 안의 첫 번째 내용 추출
            String boldContent = extractBoldContent(processedContent);
            if (boldContent != null && boldContent.length() > 5) {
                return boldContent;
            }

            // 3순위: HTML 태그 제거 후 첫 번째 문장
            return extractFirstSentence(processedContent);

        } catch (Exception e) {
            log.error("마케팅 팁 요약 생성 중 오류", e);
            return "마케팅 팁이 생성되었습니다.";
        }
    }

    /**
     * JSON이나 특수 형식 전처리
     */
    private String preprocessContent(String content) {
        // 먼저 JSON 이스케이프 문자 정리
        if (content.contains("\\n")) {
            content = content.replaceAll("\\\\n", "\n");
        }

        // JSON 구조에서 실제 HTML 내용만 추출
        if (content.contains("```html")) {
            content = content.replaceAll("```html", "")
                    .replaceAll("```", "")
                    .replaceAll("\"", "");
        }

        return content.trim();
    }

    /**
     * HTML 블록 밖의 첫 번째 제목 라인 추출
     * ```html 이후 첫 번째 줄의 내용만 추출
     */
    private String extractTitleOutsideHtml(String content) {
        // 먼저 이스케이프 문자 정리
        String processedContent = content.replaceAll("\\\\n", "\n");

        // ```html 패턴 찾기 (이스케이프 처리 후)
        String[] htmlPatterns = {"```html\n", "```html\\n"};

        for (String pattern : htmlPatterns) {
            int htmlStart = processedContent.indexOf(pattern);
            if (htmlStart != -1) {
                // 패턴 이후부터 시작
                int contentStart = htmlStart + pattern.length();

                // 첫 번째 줄바꿈까지 또는 \n\n까지 찾기
                String remaining = processedContent.substring(contentStart);
                String[] lines = remaining.split("\n");

                if (lines.length > 0) {
                    String firstLine = lines[0].trim();

                    // 유효한 내용인지 확인
                    if (firstLine.length() > 5 && !firstLine.contains("🎯") && !firstLine.contains("<")) {
                        return cleanText(firstLine);
                    }
                }
            }
        }

        // 기존 방식으로 fallback
        return extractFromLines(processedContent);
    }

    /**
     * 줄별로 처리하는 기존 방식
     */
    private String extractFromLines(String content) {
        String[] lines = content.split("\n");

        for (String line : lines) {
            line = line.trim();

            // 빈 줄이나 HTML 태그, 이모지로 시작하는 줄 건너뛰기
            if (line.isEmpty() ||
                    line.contains("<") ||
                    line.startsWith("🎯") ||
                    line.startsWith("🔍") ||
                    line.equals("```html") ||
                    line.matches("^[\\p{So}\\p{Sk}\\s]+$")) {
                continue;
            }

            // 의미있는 제목 라인 발견
            if (line.length() > 5) {
                return cleanText(line);
            }
        }

        return null;
    }

    /**
     * <b> 태그 안의 첫 번째 내용 추출
     */
    private String extractBoldContent(String htmlContent) {
        int startIndex = htmlContent.indexOf("<b>");
        if (startIndex == -1) {
            return null;
        }

        int endIndex = htmlContent.indexOf("</b>", startIndex);
        if (endIndex == -1) {
            return null;
        }

        String content = htmlContent.substring(startIndex + 3, endIndex).trim();
        return cleanText(content);
    }

    /**
     * 텍스트 정리
     */
    private String cleanText(String text) {
        if (text == null) {
            return null;
        }

        return text.replaceAll("&nbsp;", " ")
                .replaceAll("\\s+", " ")
                .trim();
    }

    /**
     * HTML 태그 제거 후 첫 번째 의미있는 문장 추출
     */
    private String extractFirstSentence(String htmlContent) {
        // HTML 태그 모두 제거
        String cleanContent = htmlContent.replaceAll("<[^>]+>", "").trim();

        // 줄별로 나누어서 첫 번째 의미있는 줄 찾기
        String[] lines = cleanContent.split("\\n");

        for (String line : lines) {
            line = line.trim();

            // 빈 줄이나 이모지만 있는 줄 건너뛰기
            if (line.isEmpty() || line.matches("^[\\p{So}\\p{Sk}\\s]+$")) {
                continue;
            }

            // 최소 길이 체크하고 반환
            if (line.length() > 5) {
                // 50자 제한
                if (line.length() > 50) {
                    return line.substring(0, 50).trim() + "...";
                }
                return line;
            }
        }

        // 모든 방법이 실패하면 기존 방식 사용
        String[] sentences = cleanContent.split("[.!?]");
        String firstSentence = sentences.length > 0 ? sentences[0].trim() : cleanContent;

        if (firstSentence.length() > 50) {
            firstSentence = firstSentence.substring(0, 50).trim() + "...";
        }

        return firstSentence.isEmpty() ? "마케팅 팁이 생성되었습니다." : firstSentence;
    }

    /**
     * 현재 로그인된 사용자 ID 조회
     */
    private String getCurrentUserId() {
        return SecurityContextHolder.getContext().getAuthentication().getName();
    }
}