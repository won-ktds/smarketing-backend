package com.won.smarketing.recommend.presentation.controller;

import com.won.smarketing.common.dto.ApiResponse;
import com.won.smarketing.recommend.application.usecase.MarketingTipUseCase;
import com.won.smarketing.recommend.presentation.dto.MarketingTipResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;

/**
 * AI 마케팅 추천 컨트롤러 (단일 API)
 */
@Tag(name = "AI 추천", description = "AI 기반 마케팅 팁 추천 API")
@Slf4j
@RestController
@RequestMapping("/api/recommend")
@RequiredArgsConstructor
public class RecommendationController {

    private final MarketingTipUseCase marketingTipUseCase;

    @Operation(
            summary = "마케팅 팁 조회/생성",
            description = "마케팅 팁 전체 내용 조회. 1시간 이내 생성된 팁이 있으면 기존 것 사용, 없으면 새로 생성"
    )
    @PostMapping("/marketing-tips")
    public ResponseEntity<ApiResponse<MarketingTipResponse>> provideMarketingTip() {

        log.info("마케팅 팁 제공 요청");

        MarketingTipResponse response = marketingTipUseCase.provideMarketingTip();

        log.info("마케팅 팁 제공 완료: tipId={}", response.getTipId());
        return ResponseEntity.ok(ApiResponse.success(response));
    }
}
