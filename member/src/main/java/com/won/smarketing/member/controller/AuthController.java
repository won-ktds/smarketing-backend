package com.won.smarketing.member.controller;

import com.won.smarketing.common.dto.ApiResponse;
import com.won.smarketing.member.dto.LoginRequest;
import com.won.smarketing.member.dto.LoginResponse;
import com.won.smarketing.member.dto.LogoutRequest;
import com.won.smarketing.member.dto.TokenRefreshRequest;
import com.won.smarketing.member.dto.TokenResponse;
import com.won.smarketing.member.service.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;


/**
 * 인증/인가를 위한 REST API 컨트롤러
 * 로그인, 로그아웃, 토큰 갱신 기능 제공
 */
@Tag(name = "인증/인가", description = "로그인, 로그아웃, 토큰 관리 API")
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    /**
     * 로그인 인증
     * 
     * @param request 로그인 요청 정보
     * @return JWT 토큰 정보
     */
    @Operation(summary = "로그인", description = "사용자 인증 후 JWT 토큰을 발급합니다.")
    @PostMapping("/login")
    public ResponseEntity<ApiResponse<LoginResponse>> login(@Valid @RequestBody LoginRequest request) {
        LoginResponse response = authService.login(request);
        return ResponseEntity.ok(ApiResponse.success(response, "로그인이 완료되었습니다."));
    }

    /**
     * 로그아웃 처리
     * 
     * @param request 로그아웃 요청 정보
     * @return 로그아웃 성공 응답
     */
    @Operation(summary = "로그아웃", description = "사용자를 로그아웃하고 토큰을 무효화합니다.")
    @PostMapping("/logout")
    public ResponseEntity<ApiResponse<Void>> logout(@Valid @RequestBody LogoutRequest request) {
        authService.logout(request.getRefreshToken());
        return ResponseEntity.ok(ApiResponse.success(null, "로그아웃이 완료되었습니다."));
    }

    /**
     * 토큰 갱신
     * 
     * @param request 토큰 갱신 요청 정보
     * @return 새로운 JWT 토큰 정보
     */
    @Operation(summary = "토큰 갱신", description = "Refresh Token을 사용하여 새로운 Access Token을 발급합니다.")
    @PostMapping("/refresh")
    public ResponseEntity<ApiResponse<TokenResponse>> refresh(@Valid @RequestBody TokenRefreshRequest request) {
        TokenResponse response = authService.refresh(request.getRefreshToken());
        return ResponseEntity.ok(ApiResponse.success(response, "토큰이 갱신되었습니다."));
    }
}
