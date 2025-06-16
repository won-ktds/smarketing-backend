package com.won.smarketing.recommend.presentation.controller;

import com.won.smarketing.common.dto.ApiResponse;
import com.won.smarketing.recommend.application.usecase.MarketingTipUseCase;
import com.won.smarketing.recommend.presentation.dto.MarketingTipRequest;
import com.won.smarketing.recommend.presentation.dto.MarketingTipResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;

/**
 * AI 마케팅 추천 컨트롤러
 */
@Tag(name = "AI 추천", description = "AI 기반 마케팅 팁 추천 API")
@Slf4j
@RestController
@RequestMapping("/api/recommendations")
@RequiredArgsConstructor
public class RecommendationController {

    private final MarketingTipUseCase marketingTipUseCase;

    @Operation(
        summary = "AI 마케팅 팁 생성",
        description = "매장 정보를 기반으로 Python AI 서비스에서 마케팅 팁을 생성합니다."
    )
    @PostMapping("/marketing-tips")
    public ResponseEntity<ApiResponse<MarketingTipResponse>> generateMarketingTips(
            @Parameter(description = "마케팅 팁 생성 요청") @Valid @RequestBody MarketingTipRequest request) {
        
        log.info("AI 마케팅 팁 생성 요청: storeId={}", request.getStoreId());
        
        MarketingTipResponse response = marketingTipUseCase.generateMarketingTips(request);
        
        log.info("AI 마케팅 팁 생성 완료: tipId={}", response.getTipId());
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @Operation(
        summary = "마케팅 팁 이력 조회",
        description = "특정 매장의 마케팅 팁 생성 이력을 조회합니다."
    )
    @GetMapping("/marketing-tips")
    public ResponseEntity<ApiResponse<Page<MarketingTipResponse>>> getMarketingTipHistory(
            @Parameter(description = "매장 ID") @RequestParam Long storeId,
            Pageable pageable) {

        log.info("마케팅 팁 이력 조회: storeId={}, page={}", storeId, pageable.getPageNumber());

        Page<MarketingTipResponse> response = marketingTipUseCase.getMarketingTipHistory(storeId, pageable);

        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @Operation(
        summary = "마케팅 팁 상세 조회",
        description = "특정 마케팅 팁의 상세 정보를 조회합니다."
    )
    @GetMapping("/marketing-tips/{tipId}")
    public ResponseEntity<ApiResponse<MarketingTipResponse>> getMarketingTip(
            @Parameter(description = "팁 ID") @PathVariable Long tipId) {
        
        log.info("마케팅 팁 상세 조회: tipId={}", tipId);
        
        MarketingTipResponse response = marketingTipUseCase.getMarketingTip(tipId);
        
        return ResponseEntity.ok(ApiResponse.success(response));
    }
}
