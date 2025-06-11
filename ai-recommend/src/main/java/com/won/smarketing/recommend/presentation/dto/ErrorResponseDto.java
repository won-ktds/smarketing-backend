package com.won.smarketing.recommend.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 에러 응답 DTO
 * AI 추천 서비스에서 발생하는 에러 정보를 전달합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "에러 응답")
public class ErrorResponseDto {
    
    @Schema(description = "에러 코드", example = "AI_SERVICE_ERROR")
    private String errorCode;
    
    @Schema(description = "에러 메시지", example = "AI 서비스 연결에 실패했습니다")
    private String message;
    
    @Schema(description = "에러 발생 시간", example = "2024-01-15T10:30:00")
    private LocalDateTime timestamp;
    
    @Schema(description = "요청 경로", example = "/api/recommendation/marketing-tips")
    private String path;
}

