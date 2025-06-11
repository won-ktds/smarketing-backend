package com.won.smarketing.member.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 로그인 응답 DTO
 * 로그인 성공 시 토큰 정보를 전달합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "로그인 응답")
public class LoginResponse {
    
    @Schema(description = "액세스 토큰", example = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    private String accessToken;
    
    @Schema(description = "리프레시 토큰", example = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    private String refreshToken;
    
    @Schema(description = "토큰 만료 시간 (초)", example = "3600")
    private long expiresIn;
    
    @Schema(description = "사용자 정보")
    private UserInfo userInfo;
    
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Schema(description = "사용자 정보")
    public static class UserInfo {
        @Schema(description = "사용자 ID", example = "user123")
        private String userId;
        
        @Schema(description = "이름", example = "홍길동")
        private String name;
        
        @Schema(description = "이메일", example = "user@example.com")
        private String email;
    }
}
