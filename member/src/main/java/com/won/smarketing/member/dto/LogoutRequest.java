package com.won.smarketing.member.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.validation.constraints.NotBlank;

/**
 * 로그아웃 요청 DTO
 * 로그아웃 시 무효화할 Refresh Token 정보
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "로그아웃 요청")
public class LogoutRequest {

    @Schema(description = "무효화할 Refresh Token", example = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", required = true)
    @NotBlank(message = "Refresh Token은 필수입니다.")
    private String refreshToken;
}
