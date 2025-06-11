package com.won.smarketing.member.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.validation.constraints.NotBlank;

/**
 * 로그인 요청 DTO
 * 로그인 시 필요한 사용자 ID와 패스워드 정보
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "로그인 요청 정보")
public class LoginRequest {

    @Schema(description = "사용자 ID", example = "testuser", required = true)
    @NotBlank(message = "사용자 ID는 필수입니다.")
    private String userId;

    @Schema(description = "패스워드", example = "password123!", required = true)
    @NotBlank(message = "패스워드는 필수입니다.")
    private String password;
}
