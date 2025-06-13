package com.won.smarketing.member.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 중복 확인 응답 DTO
 * 사용자 ID, 이메일 등의 중복 확인 결과를 전달합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "중복 확인 응답")
public class DuplicateCheckResponse {
    
    @Schema(description = "중복 여부", example = "false")
    private boolean isDuplicate;
    
    @Schema(description = "메시지", example = "사용 가능한 ID입니다.")
    private String message;
    
    /**
     * 중복된 경우의 응답 생성
     * 
     * @param message 메시지
     * @return 중복 응답
     */
    public static DuplicateCheckResponse duplicate(String message) {
        return DuplicateCheckResponse.builder()
                .isDuplicate(true)
                .message(message)
                .build();
    }
    
    /**
     * 사용 가능한 경우의 응답 생성
     * 
     * @param message 메시지
     * @return 사용 가능 응답
     */
    public static DuplicateCheckResponse available(String message) {
        return DuplicateCheckResponse.builder()
                .isDuplicate(false)
                .message(message)
                .build();
    }
}



