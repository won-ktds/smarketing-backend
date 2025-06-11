package com.won.smarketing.common.security;

import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.util.Date;

/**
 * JWT 토큰 생성 및 검증을 담당하는 클래스
 * 액세스 토큰과 리프레시 토큰의 생성, 검증, 파싱 기능 제공
 */
@Slf4j
@Component
public class JwtTokenProvider {

    private final SecretKey secretKey;
    private final long accessTokenValidityTime;
    private final long refreshTokenValidityTime;

    /**
     * JWT 토큰 프로바이더 생성자
     * 
     * @param secret JWT 서명에 사용할 비밀키
     * @param accessTokenValidityTime 액세스 토큰 유효시간 (밀리초)
     * @param refreshTokenValidityTime 리프레시 토큰 유효시간 (밀리초)
     */
    public JwtTokenProvider(@Value("${jwt.secret}") String secret,
                           @Value("${jwt.access-token-validity}") long accessTokenValidityTime,
                           @Value("${jwt.refresh-token-validity}") long refreshTokenValidityTime) {
        this.secretKey = Keys.hmacShaKeyFor(secret.getBytes());
        this.accessTokenValidityTime = accessTokenValidityTime;
        this.refreshTokenValidityTime = refreshTokenValidityTime;
    }

    /**
     * 액세스 토큰 생성
     * 
     * @param userId 사용자 ID
     * @return 생성된 액세스 토큰
     */
    public String generateAccessToken(String userId) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + accessTokenValidityTime);

        return Jwts.builder()
                .setSubject(userId)
                .setIssuedAt(now)
                .setExpiration(expiryDate)
                .signWith(secretKey)
                .compact();
    }

    /**
     * 리프레시 토큰 생성
     * 
     * @param userId 사용자 ID
     * @return 생성된 리프레시 토큰
     */
    public String generateRefreshToken(String userId) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + refreshTokenValidityTime);

        return Jwts.builder()
                .setSubject(userId)
                .setIssuedAt(now)
                .setExpiration(expiryDate)
                .signWith(secretKey)
                .compact();
    }

    /**
     * 토큰에서 사용자 ID 추출
     * 
     * @param token JWT 토큰
     * @return 사용자 ID
     */
    public String getUserIdFromToken(String token) {
        Claims claims = Jwts.parserBuilder()
                .setSigningKey(secretKey)
                .build()
                .parseClaimsJws(token)
                .getBody();
        
        return claims.getSubject();
    }

    /**
     * 토큰 유효성 검증
     * 
     * @param token 검증할 토큰
     * @return 유효성 여부
     */
    public boolean validateToken(String token) {
        try {
            Jwts.parserBuilder()
                    .setSigningKey(secretKey)
                    .build()
                    .parseClaimsJws(token);
            return true;
        } catch (SecurityException ex) {
            log.error("Invalid JWT signature: {}", ex.getMessage());
        } catch (MalformedJwtException ex) {
            log.error("Invalid JWT token: {}", ex.getMessage());
        } catch (ExpiredJwtException ex) {
            log.error("Expired JWT token: {}", ex.getMessage());
        } catch (UnsupportedJwtException ex) {
            log.error("Unsupported JWT token: {}", ex.getMessage());
        } catch (IllegalArgumentException ex) {
            log.error("JWT claims string is empty: {}", ex.getMessage());
        }
        return false;
    }

    /**
     * 액세스 토큰 유효시간 반환
     * 
     * @return 액세스 토큰 유효시간 (밀리초)
     */
    public long getAccessTokenValidityTime() {
        return accessTokenValidityTime;
    }
}
