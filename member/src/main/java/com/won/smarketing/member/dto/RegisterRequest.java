package com.won.smarketing.member.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;
import javax.validation.constraints.Size;

/**
 * 회원가입 요청 DTO
 * 회원가입 시 필요한 정보를 담는 데이터 전송 객체
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "회원가입 요청 정보")
public class RegisterRequest {

    @Schema(description = "사용자 ID", example = "testuser", required = true)
    @NotBlank(message = "사용자 ID는 필수입니다.")
    @Size(min = 4, max = 20, message = "사용자 ID는 4자 이상 20자 이하여야 합니다.")
    @Pattern(regexp = "^[a-zA-Z0-9]+$", message = "사용자 ID는 영문과 숫자만 가능합니다.")
    private String userId;

    @Schema(description = "패스워드", example = "password123!", required = true)
    @NotBlank(message = "패스워드는 필수입니다.")
    private String password;

    @Schema(description = "이름", example = "홍길동", required = true)
    @NotBlank(message = "이름은 필수입니다.")
    @Size(max = 100, message = "이름은 100자 이하여야 합니다.")
    private String name;

    @Schema(description = "사업자 번호", example = "123-45-67890", required = true)
    @NotBlank(message = "사업자 번호는 필수입니다.")
    @Pattern(regexp = "^\\d{3}-\\d{2}-\\d{5}$", message = "사업자 번호 형식이 올바르지 않습니다.")
    private String businessNumber;

    @Schema(description = "이메일", example = "test@example.com", required = true)
    @NotBlank(message = "이메일은 필수입니다.")
    @Email(message = "올바른 이메일 형식이 아닙니다.")
    private String email;
}
