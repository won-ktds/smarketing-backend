package com.won.smarketing.member.service;

import com.won.smarketing.member.dto.LoginRequest;
import com.won.smarketing.member.dto.LoginResponse;
import com.won.smarketing.member.dto.TokenResponse;

/**
 * 인증 서비스 인터페이스
 * 로그인, 로그아웃, 토큰 갱신 관련 비즈니스 로직 정의
 */
public interface AuthService {
    
    /**
     * 로그인
     * 
     * @param request 로그인 요청 정보
     * @return 로그인 응답 정보 (토큰 포함)
     */
    LoginResponse login(LoginRequest request);
    
    /**
     * 로그아웃
     * 
     * @param refreshToken 리프레시 토큰
     */
    void logout(String refreshToken);
    
    /**
     * 토큰 갱신
     * 
     * @param refreshToken 리프레시 토큰
     * @return 새로운 토큰 정보
     */
    TokenResponse refresh(String refreshToken);
}
