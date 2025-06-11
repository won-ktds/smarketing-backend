package com.won.smarketing.member.service;

import com.won.smarketing.member.dto.LoginRequest;
import com.won.smarketing.member.dto.LoginResponse;
import com.won.smarketing.member.dto.TokenResponse;

/**
 * 인증/인가 서비스 인터페이스
 * 로그인, 로그아웃, 토큰 갱신 기능 정의
 */
public interface AuthService {
    
    /**
     * 로그인 인증 처리
     * 
     * @param request 로그인 요청 정보
     * @return JWT 토큰 정보
     */
    LoginResponse login(LoginRequest request);
    
    /**
     * 로그아웃 처리
     * 
     * @param refreshToken 무효화할 Refresh Token
     */
    void logout(String refreshToken);
    
    /**
     * 토큰 갱신 처리
     * 
     * @param refreshToken 갱신에 사용할 Refresh Token
     * @return 새로운 JWT 토큰 정보
     */
    TokenResponse refresh(String refreshToken);
}
