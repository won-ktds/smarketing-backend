package com.won.smarketing.member.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 로그인 요청 DTO
 * 로그인 시 필요한 정보를 전달합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "로그인 요청")
public class LoginRequest {
    
    @Schema(description = "사용자 ID", example = "user123", required = true)
    @NotBlank(message = "사용자 ID는 필수입니다")
    private String userId;
    
    @Schema(description = "패스워드", example = "password123!", required = true)
    @NotBlank(message = "패스워드는 필수입니다")
    private String password;
}
