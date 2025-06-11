package com.won.smarketing.member.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * ID 중복 확인 응답 DTO
 * 사용자 ID 중복 여부 확인 결과
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "ID 중복 확인 응답")
public class DuplicateCheckResponse {

    @Schema(description = "중복 여부", example = "false")
    private boolean isDuplicate;

    @Schema(description = "확인 결과 메시지", example = "사용 가능한 ID입니다.")
    private String message;
}
