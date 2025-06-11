package com.won.smarketing.member.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 토큰 응답 DTO
 * 토큰 갱신 시 새로운 토큰 정보를 전달합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "토큰 응답")
public class TokenResponse {
    
    @Schema(description = "새로운 액세스 토큰", example = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    private String accessToken;
    
    @Schema(description = "새로운 리프레시 토큰", example = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    private String refreshToken;
    
    @Schema(description = "토큰 만료 시간 (초)", example = "3600")
    private long expiresIn;
}
