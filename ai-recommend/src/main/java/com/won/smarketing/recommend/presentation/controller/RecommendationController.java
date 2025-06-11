package com.won.smarketing.recommend.presentation.controller;

import com.won.smarketing.common.dto.ApiResponse;
import com.won.smarketing.recommend.application.usecase.MarketingTipUseCase;
import com.won.smarketing.recommend.presentation.dto.MarketingTipRequest;
import com.won.smarketing.recommend.presentation.dto.MarketingTipResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;


/**
 * AI 마케팅 추천을 위한 REST API 컨트롤러
 * AI 기반 마케팅 팁 생성 기능 제공
 */
@Tag(name = "AI 마케팅 추천", description = "AI 기반 맞춤형 마케팅 추천 API")
@RestController
@RequestMapping("/api/recommendation")
@RequiredArgsConstructor
public class RecommendationController {

    private final MarketingTipUseCase marketingTipUseCase;

    /**
     * AI 마케팅 팁 생성
     * 
     * @param request 마케팅 팁 생성 요청
     * @return 생성된 마케팅 팁
     */
    @Operation(summary = "AI 마케팅 팁 생성", description = "매장 특성과 환경 정보를 바탕으로 AI 마케팅 팁을 생성합니다.")
    @PostMapping("/marketing-tips")
    public ResponseEntity<ApiResponse<MarketingTipResponse>> generateMarketingTips(@Valid @RequestBody MarketingTipRequest request) {
        MarketingTipResponse response = marketingTipUseCase.generateMarketingTips(request);
        return ResponseEntity.ok(ApiResponse.success(response, "AI 마케팅 팁이 성공적으로 생성되었습니다."));
    }
}
