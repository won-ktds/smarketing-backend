package com.won.smarketing.member.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 패스워드 검증 요청 DTO
 * 패스워드 규칙 검증을 위한 요청 정보를 전달합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "패스워드 검증 요청")
public class PasswordValidationRequest {
    
    @Schema(description = "검증할 패스워드", example = "password123!", required = true)
    @NotBlank(message = "패스워드는 필수입니다")
    private String password;
}
