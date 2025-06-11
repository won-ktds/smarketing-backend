package com.won.smarketing.member.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * 검증 응답 DTO
 * 패스워드 등의 검증 결과를 전달합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "검증 응답")
public class ValidationResponse {
    
    @Schema(description = "유효성 여부", example = "true")
    private boolean isValid;
    
    @Schema(description = "메시지", example = "사용 가능한 패스워드입니다.")
    private String message;
    
    @Schema(description = "오류 목록", example = "[\"영문이 포함되어야 합니다\", \"숫자가 포함되어야 합니다\"]")
    private List<String> errors;
    
    /**
     * 유효한 경우의 응답 생성
     * 
     * @param message 메시지
     * @return 유효 응답
     */
    public static ValidationResponse valid(String message) {
        return ValidationResponse.builder()
                .isValid(true)
                .message(message)
                .build();
    }
    
    /**
     * 유효하지 않은 경우의 응답 생성
     * 
     * @param message 메시지
     * @param errors 오류 목록
     * @return 무효 응답
     */
    public static ValidationResponse invalid(String message, List<String> errors) {
        return ValidationResponse.builder()
                .isValid(false)
                .message(message)
                .errors(errors)
                .build();
    }
}
