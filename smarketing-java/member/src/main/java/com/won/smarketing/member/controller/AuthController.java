package com.won.smarketing.member.controller;

import com.won.smarketing.common.dto.ApiResponse;
import com.won.smarketing.member.dto.*;
import com.won.smarketing.member.service.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;

/**
 * 인증을 위한 REST API 컨트롤러
 * 로그인, 로그아웃, 토큰 갱신 기능 제공
 */
@Tag(name = "인증 관리", description = "로그인, 로그아웃, 토큰 관리 API")
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    /**
     * 로그인
     * 
     * @param request 로그인 요청 정보
     * @return 로그인 성공 응답 (토큰 포함)
     */
    @Operation(summary = "로그인", description = "사용자 ID와 패스워드로 로그인합니다.")
    @PostMapping("/login")
    public ResponseEntity<ApiResponse<LoginResponse>> login(@Valid @RequestBody LoginRequest request) {
        LoginResponse response = authService.login(request);
        return ResponseEntity.ok(ApiResponse.success(response, "로그인이 완료되었습니다."));
    }

    /**
     * 로그아웃
     * 
     * @param request 로그아웃 요청 정보
     * @return 로그아웃 성공 응답
     */
    @Operation(summary = "로그아웃", description = "리프레시 토큰을 무효화하여 로그아웃합니다.")
    @PostMapping("/logout")
    public ResponseEntity<ApiResponse<Void>> logout(@Valid @RequestBody LogoutRequest request) {
        authService.logout(request.getRefreshToken());
        return ResponseEntity.ok(ApiResponse.success(null, "로그아웃이 완료되었습니다."));
    }

    /**
     * 토큰 갱신
     * 
     * @param request 토큰 갱신 요청 정보
     * @return 새로운 토큰 정보
     */
    @Operation(summary = "토큰 갱신", description = "리프레시 토큰을 사용하여 새로운 액세스 토큰을 발급받습니다.")
    @PostMapping("/refresh")
    public ResponseEntity<ApiResponse<TokenResponse>> refresh(@Valid @RequestBody TokenRefreshRequest request) {
        TokenResponse response = authService.refresh(request.getRefreshToken());
        return ResponseEntity.ok(ApiResponse.success(response, "토큰이 갱신되었습니다."));
    }
}
