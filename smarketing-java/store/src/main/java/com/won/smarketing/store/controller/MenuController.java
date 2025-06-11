package com.won.smarketing.store.controller;

import com.won.smarketing.common.dto.ApiResponse;
import com.won.smarketing.store.dto.MenuCreateRequest;
import com.won.smarketing.store.dto.MenuResponse;
import com.won.smarketing.store.dto.MenuUpdateRequest;
import com.won.smarketing.store.service.MenuService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;

/**
 * 메뉴 관리를 위한 REST API 컨트롤러
 * 메뉴 등록, 조회, 수정, 삭제 기능 제공
 */
@Tag(name = "메뉴 관리", description = "메뉴 정보 관리 API")
@RestController
@RequestMapping("/api/menu")
@RequiredArgsConstructor
public class MenuController {

    private final MenuService menuService;

    /**
     * 메뉴 정보 등록
     * 
     * @param request 메뉴 등록 요청 정보
     * @return 등록된 메뉴 정보
     */
    @Operation(summary = "메뉴 등록", description = "새로운 메뉴를 등록합니다.")
    @PostMapping("/register")
    public ResponseEntity<ApiResponse<MenuResponse>> register(@Valid @RequestBody MenuCreateRequest request) {
        MenuResponse response = menuService.register(request);
        return ResponseEntity.ok(ApiResponse.success(response, "메뉴가 성공적으로 등록되었습니다."));
    }

    /**
     * 메뉴 목록 조회
     * 
     * @param category 메뉴 카테고리 (선택사항)
     * @return 메뉴 목록
     */
    @Operation(summary = "메뉴 목록 조회", description = "메뉴 목록을 조회합니다. 카테고리별 필터링 가능합니다.")
    @GetMapping
    public ResponseEntity<ApiResponse<List<MenuResponse>>> getMenus(
            @Parameter(description = "메뉴 카테고리")
            @RequestParam(required = false) String category) {
        List<MenuResponse> response = menuService.getMenus(category);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    /**
     * 메뉴 정보 수정
     * 
     * @param menuId 수정할 메뉴 ID
     * @param request 메뉴 수정 요청 정보
     * @return 수정된 메뉴 정보
     */
    @Operation(summary = "메뉴 수정", description = "메뉴 정보를 수정합니다.")
    @PutMapping("/{menuId}")
    public ResponseEntity<ApiResponse<MenuResponse>> updateMenu(
            @Parameter(description = "메뉴 ID", required = true)
            @PathVariable Long menuId,
            @Valid @RequestBody MenuUpdateRequest request) {
        MenuResponse response = menuService.updateMenu(menuId, request);
        return ResponseEntity.ok(ApiResponse.success(response, "메뉴가 성공적으로 수정되었습니다."));
    }

    /**
     * 메뉴 삭제
     * 
     * @param menuId 삭제할 메뉴 ID
     * @return 삭제 성공 응답
     */
    @Operation(summary = "메뉴 삭제", description = "메뉴를 삭제합니다.")
    @DeleteMapping("/{menuId}")
    public ResponseEntity<ApiResponse<Void>> deleteMenu(
            @Parameter(description = "메뉴 ID", required = true)
            @PathVariable Long menuId) {
        menuService.deleteMenu(menuId);
        return ResponseEntity.ok(ApiResponse.success(null, "메뉴가 성공적으로 삭제되었습니다."));
    }
}
