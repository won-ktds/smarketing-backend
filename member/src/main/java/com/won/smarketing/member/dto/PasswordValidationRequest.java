package com.won.smarketing.member.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.validation.constraints.NotBlank;

/**
 * 패스워드 유효성 검증 요청 DTO
 * 패스워드 보안 규칙 확인을 위한 요청 정보
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "패스워드 유효성 검증 요청")
public class PasswordValidationRequest {

    @Schema(description = "검증할 패스워드", example = "password123!", required = true)
    @NotBlank(message = "패스워드는 필수입니다.")
    private String password;
}
