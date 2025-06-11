package com.won.smarketing.member.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * 유효성 검증 응답 DTO
 * 패스워드 유효성 검증 결과 정보
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "유효성 검증 응답")
public class ValidationResponse {

    @Schema(description = "유효성 여부", example = "true")
    private boolean isValid;

    @Schema(description = "검증 결과 메시지", example = "유효한 패스워드입니다.")
    private String message;

    @Schema(description = "오류 목록")
    private List<String> errors;
}
