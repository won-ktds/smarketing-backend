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
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.concurrent.TimeUnit;

/**
 * 인증 서비스 구현체
 * 로그인, 로그아웃, 토큰 갱신 기능 구현
 */
@Slf4j
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class AuthServiceImpl implements AuthService {

        private final MemberRepository memberRepository;
        private final PasswordEncoder passwordEncoder;
        private final JwtTokenProvider jwtTokenProvider;
        private final RedisTemplate<String, String> redisTemplate;

        private static final String REFRESH_TOKEN_PREFIX = "refresh_token:";
        private static final String BLACKLIST_PREFIX = "blacklist:";

        /**
         * 로그인
         *
         * @param request 로그인 요청 정보
         * @return 로그인 응답 정보 (토큰 포함)
         */
        @Override
        @Transactional
        public LoginResponse login(LoginRequest request) {
                log.info("로그인 시도: {}", request.getUserId());

                // 회원 조회
                Member member = memberRepository.findByUserId(request.getUserId())
                        .orElseThrow(() -> new BusinessException(ErrorCode.MEMBER_NOT_FOUND));

                // 패스워드 검증
                if (!passwordEncoder.matches(request.getPassword(), member.getPassword())) {
                        System.out.println(passwordEncoder.encode(request.getPassword()));
                        System.out.println(passwordEncoder.encode(member.getPassword()));

                        throw new BusinessException(ErrorCode.INVALID_PASSWORD);
                }

                // 토큰 생성
                String accessToken = jwtTokenProvider.generateAccessToken(member.getUserId());
                String refreshToken = jwtTokenProvider.generateRefreshToken(member.getUserId());

                log.info("{} access token 발급: {}", request.getUserId(), accessToken);

                // 리프레시 토큰을 Redis에 저장 (7일)
                redisTemplate.opsForValue().set(
                        REFRESH_TOKEN_PREFIX + member.getUserId(),
                        refreshToken,
                        7,
                        TimeUnit.DAYS
                );

                log.info("로그인 성공: {}", request.getUserId());

                return LoginResponse.builder()
                        .accessToken(accessToken)
                        .refreshToken(refreshToken)
                        .expiresIn(jwtTokenProvider.getAccessTokenValidityTime() / 1000)
                        .userInfo(LoginResponse.UserInfo.builder()
                                .userId(member.getUserId())
                                .name(member.getName())
                                .email(member.getEmail())
                                .build())
                        .build();
        }

        /**
         * 로그아웃
         *
         * @param refreshToken 리프레시 토큰
         */
        @Override
        @Transactional
        public void logout(String refreshToken) {
                try {
                        if (jwtTokenProvider.validateToken(refreshToken)) {
                                String userId = jwtTokenProvider.getUserIdFromToken(refreshToken);

                                redisTemplate.delete(REFRESH_TOKEN_PREFIX + userId);

                                log.info("로그아웃 완료: {}", userId);
                        }
                } catch (Exception ex) {
                        log.warn("로그아웃 처리 중 오류 발생: {}", ex.getMessage());
                        // 로그아웃은 실패해도 클라이언트에게는 성공으로 응답
                }
        }

        /**
         * 토큰 갱신
         *
         * @param refreshToken 리프레시 토큰
         * @return 새로운 토큰 정보
         */
        @Override
        @Transactional
        public TokenResponse refresh(String refreshToken) {
                // 토큰 유효성 검증
                if (!jwtTokenProvider.validateToken(refreshToken)) {
                        throw new BusinessException(ErrorCode.INVALID_TOKEN);
                }

                // 블랙리스트 확인
                if (redisTemplate.hasKey(BLACKLIST_PREFIX + refreshToken)) {
                        throw new BusinessException(ErrorCode.INVALID_TOKEN);
                }

                String userId = jwtTokenProvider.getUserIdFromToken(refreshToken);

                // Redis에 저장된 리프레시 토큰과 비교
                String storedRefreshToken = redisTemplate.opsForValue().get(REFRESH_TOKEN_PREFIX + userId);
                if (!refreshToken.equals(storedRefreshToken)) {
                        throw new BusinessException(ErrorCode.INVALID_TOKEN);
                }

                // 회원 존재 확인
                if (!memberRepository.existsByUserId(userId)) {
                        throw new BusinessException(ErrorCode.MEMBER_NOT_FOUND);
                }

                // 새로운 토큰 생성
                String newAccessToken = jwtTokenProvider.generateAccessToken(userId);
                String newRefreshToken = jwtTokenProvider.generateRefreshToken(userId);

                // 새로운 리프레시 토큰을 Redis에 저장
                redisTemplate.opsForValue().set(
                        REFRESH_TOKEN_PREFIX + userId,
                        newRefreshToken,
                        7,
                        TimeUnit.DAYS
                );

                // 기존 리프레시 토큰 삭제
                redisTemplate.delete(REFRESH_TOKEN_PREFIX + userId);

                log.info("토큰 갱신 완료: {}", userId);

                return TokenResponse.builder()
                        .accessToken(newAccessToken)
                        .refreshToken(newRefreshToken)
                        .expiresIn(jwtTokenProvider.getAccessTokenValidityTime() / 1000)
                        .build();
        }
}