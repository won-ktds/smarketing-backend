package com.won.smarketing.store.controller;

import com.won.smarketing.common.dto.ApiResponse;
import com.won.smarketing.store.dto.StoreCreateRequest;
import com.won.smarketing.store.dto.StoreCreateResponse;
import com.won.smarketing.store.dto.StoreResponse;
import com.won.smarketing.store.dto.StoreUpdateRequest;
import com.won.smarketing.store.service.StoreService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;

/**
 * 매장 관리를 위한 REST API 컨트롤러
 * 매장 등록, 조회, 수정 기능 제공
 */
@Tag(name = "매장 관리", description = "매장 정보 관리 API")
@RestController
@RequestMapping("/api/store")
@RequiredArgsConstructor
public class StoreController {

    private final StoreService storeService;

    /**
     * 매장 정보 등록
     * 
     * @param request 매장 등록 요청 정보
     * @return 등록된 매장 정보
     */
    @Operation(summary = "매장 등록", description = "새로운 매장 정보를 등록합니다.")
    @PostMapping("/register")
    public ResponseEntity<ApiResponse<StoreCreateResponse>> register(@Valid @RequestBody StoreCreateRequest request) {
        StoreCreateResponse response = storeService.register(request);
        return ResponseEntity.ok(ApiResponse.success(response, "매장이 성공적으로 등록되었습니다."));
    }

    /**
     * 매장 정보 조회
     * 
     * //@param userId 조회할 매장 ID
     * @return 매장 정보
     */
    @Operation(summary = "매장 조회", description = "유저 ID로 매장 정보를 조회합니다.")
    @GetMapping
    public ResponseEntity<ApiResponse<StoreResponse>> getStore(
//            @Parameter(description = "유저 ID", required = true)
//            @RequestParam String userId
    ) {
        StoreResponse response = storeService.getStore();
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    /**
     * 매장 정보 수정
     * 
     * //@param storeId 수정할 매장 ID
     * @param request 매장 수정 요청 정보
     * @return 수정된 매장 정보
     */
    @Operation(summary = "매장 수정", description = "매장 정보를 수정합니다.")
    @PutMapping()
    public ResponseEntity<ApiResponse<StoreResponse>> updateStore(
            @Parameter(description = "매장 ID", required = true)
           // @PathVariable Long storeId,
            @Valid @RequestBody StoreUpdateRequest request) {
        StoreResponse response = storeService.updateStore(request);
        return ResponseEntity.ok(ApiResponse.success(response, "매장 정보가 성공적으로 수정되었습니다."));
    }
}
