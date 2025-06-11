package com.won.smarketing.member.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 토큰 갱신 요청 DTO
 * 리프레시 토큰을 사용한 액세스 토큰 갱신 요청 정보를 전달합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "토큰 갱신 요청")
public class TokenRefreshRequest {
    
    @Schema(description = "리프레시 토큰", example = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", required = true)
    @NotBlank(message = "리프레시 토큰은 필수입니다")
    private String refreshToken;
}
