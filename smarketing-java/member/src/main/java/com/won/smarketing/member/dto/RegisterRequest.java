package com.won.smarketing.member.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 회원가입 요청 DTO
 * 회원가입 시 필요한 정보를 전달합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "회원가입 요청")
public class RegisterRequest {
    
    @Schema(description = "사용자 ID", example = "user123", required = true)
    @NotBlank(message = "사용자 ID는 필수입니다")
    @Size(min = 4, max = 20, message = "사용자 ID는 4-20자 사이여야 합니다")
    @Pattern(regexp = "^[a-zA-Z0-9]+$", message = "사용자 ID는 영문과 숫자만 사용 가능합니다")
    private String userId;
    
    @Schema(description = "패스워드", example = "password123!", required = true)
    @NotBlank(message = "패스워드는 필수입니다")
    @Size(min = 8, max = 20, message = "패스워드는 8-20자 사이여야 합니다")
    @Pattern(regexp = "^(?=.*[a-zA-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]+$", 
             message = "패스워드는 영문, 숫자, 특수문자를 포함해야 합니다")
    private String password;
    
    @Schema(description = "이름", example = "홍길동", required = true)
    @NotBlank(message = "이름은 필수입니다")
    @Size(max = 50, message = "이름은 50자 이하여야 합니다")
    private String name;

    @Schema(description = "사업자등록번호", example = "1234567890")
    @Pattern(regexp = "^\\d{10}$", message = "사업자등록번호는 10자리 숫자여야 합니다")
    private String businessNumber;
    
    @Schema(description = "이메일", example = "user@example.com", required = true)
    @NotBlank(message = "이메일은 필수입니다")
    @Email(message = "이메일 형식이 올바르지 않습니다")
    @Size(max = 100, message = "이메일은 100자 이하여야 합니다")
    private String email;
}
