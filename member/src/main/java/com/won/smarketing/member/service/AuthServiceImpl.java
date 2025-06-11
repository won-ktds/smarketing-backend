package com.won.smarketing.member.service;

import com.won.smarketing.common.exception.BusinessException;
import com.won.smarketing.common.exception.ErrorCode;
import com.won.smarketing.common.security.JwtTokenProvider;
import com.won.smarketing.member.dto.LoginRequest;
import com.won.smarketing.member.dto.LoginResponse;
import com.won.smarketing.member.dto.TokenResponse;
import com.won.smarketing.member.entity.Member;
import com.won.smarketing.member.repository.MemberRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.concurrent.TimeUnit;

/**
 * 인증/인가 서비스 구현체
 * 로그인, 로그아웃, 토큰 갱신 기능 구현
 */
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class AuthServiceImpl implements AuthService {

    private final MemberRepository memberRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenProvider jwtTokenProvider;
    private final RedisTemplate<String, String> redisTemplate;

    private static final String REFRESH_TOKEN_PREFIX = "refresh_token:";

    /**
     * 로그인 인증 처리
     * 
     * @param request 로그인 요청 정보
     * @return JWT 토큰 정보
     */
    @Override
    @Transactional
    public LoginResponse login(LoginRequest request) {
        // 사용자 조회
        Member member = memberRepository.findByUserId(request.getUserId())
                .orElseThrow(() -> new BusinessException(ErrorCode.MEMBER_NOT_FOUND));

        // 패스워드 검증
        if (!passwordEncoder.matches(request.getPassword(), member.getPassword())) {
            throw new BusinessException(ErrorCode.INVALID_PASSWORD);
        }

        // JWT 토큰 생성
        String accessToken = jwtTokenProvider.generateAccessToken(member.getUserId());
        String refreshToken = jwtTokenProvider.generateRefreshToken(member.getUserId());
        long expiresIn = jwtTokenProvider.getAccessTokenValidityTime();

        // Refresh Token을 Redis에 저장
        String refreshTokenKey = REFRESH_TOKEN_PREFIX + member.getUserId();
        redisTemplate.opsForValue().set(refreshTokenKey, refreshToken, 
                jwtTokenProvider.getRefreshTokenValidityTime(), TimeUnit.MILLISECONDS);

        return LoginResponse.builder()
                .accessToken(accessToken)
                .refreshToken(refreshToken)
                .expiresIn(expiresIn)
                .build();
    }

    /**
     * 로그아웃 처리
     * 
     * @param refreshToken 무효화할 Refresh Token
     */
    @Override
    @Transactional
    public void logout(String refreshToken) {
        // 토큰에서 사용자 ID 추출
        String userId = jwtTokenProvider.getUserIdFromToken(refreshToken);
        
        // Redis에서 Refresh Token 삭제
        String refreshTokenKey = REFRESH_TOKEN_PREFIX + userId;
        redisTemplate.delete(refreshTokenKey);
    }

    /**
     * 토큰 갱신 처리
     * 
     * @param refreshToken 갱신에 사용할 Refresh Token
     * @return 새로운 JWT 토큰 정보
     */
    @Override
    @Transactional
    public TokenResponse refresh(String refreshToken) {
        // Refresh Token 유효성 검증
        if (!jwtTokenProvider.validateToken(refreshToken)) {
            throw new BusinessException(ErrorCode.INVALID_TOKEN);
        }

        // 토큰에서 사용자 ID 추출
        String userId = jwtTokenProvider.getUserIdFromToken(refreshToken);
        
        // Redis에서 저장된 Refresh Token 확인
        String refreshTokenKey = REFRESH_TOKEN_PREFIX + userId;
        String storedRefreshToken = redisTemplate.opsForValue().get(refreshTokenKey);
        
        if (storedRefreshToken == null || !storedRefreshToken.equals(refreshToken)) {
            throw new BusinessException(ErrorCode.INVALID_TOKEN);
        }

        // 사용자 존재 여부 확인
        Member member = memberRepository.findByUserId(userId)
                .orElseThrow(() -> new BusinessException(ErrorCode.MEMBER_NOT_FOUND));

        // 새로운 토큰 생성
        String newAccessToken = jwtTokenProvider.generateAccessToken(member.getUserId());
        String newRefreshToken = jwtTokenProvider.generateRefreshToken(member.getUserId());
        long expiresIn = jwtTokenProvider.getAccessTokenValidityTime();

        // 기존 Refresh Token 삭제 후 새로운 토큰 저장
        redisTemplate.delete(refreshTokenKey);
        redisTemplate.opsForValue().set(refreshTokenKey, newRefreshToken, 
                jwtTokenProvider.getRefreshTokenValidityTime(), TimeUnit.MILLISECONDS);

        return TokenResponse.builder()
                .accessToken(newAccessToken)
                .refreshToken(newRefreshToken)
                .expiresIn(expiresIn)
                .build();
    }
}
