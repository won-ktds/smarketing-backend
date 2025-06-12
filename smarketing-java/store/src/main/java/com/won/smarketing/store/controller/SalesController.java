package com.won.smarketing.store.controller;

import com.won.smarketing.common.dto.ApiResponse;
import com.won.smarketing.store.dto.SalesResponse;
import com.won.smarketing.store.service.SalesService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 매출 정보를 위한 REST API 컨트롤러
 * 매출 조회 기능 제공
 */
@Tag(name = "매출 관리", description = "매출 정보 조회 API")
@RestController
@RequestMapping("/api/sales")
@RequiredArgsConstructor
public class SalesController {

    private final SalesService salesService;

    /**
     * 매출 정보 조회
     * 
     * @param storeId 가게 ID
     * @return 매출 정보 (오늘, 월간, 전일 대비)
     */
    @Operation(summary = "매출 조회", description = "오늘 매출, 월간 매출, 전일 대비 매출 정보를 조회합니다.")
    @GetMapping("/{storeId}")
    public ResponseEntity<ApiResponse<SalesResponse>> getSales(
            @Parameter(description = "가게 ID", required = true)
            @PathVariable Long storeId
    ) {
        SalesResponse response = salesService.getSales(storeId);
        return ResponseEntity.ok(ApiResponse.success(response));
    }
}
