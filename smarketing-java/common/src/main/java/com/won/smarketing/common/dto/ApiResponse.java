package com.won.smarketing.common.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 표준 API 응답 DTO
 * 모든 API 응답에 사용되는 공통 형식
 * 
 * @param <T> 응답 데이터 타입
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "API 응답")
public class ApiResponse<T> {

    @Schema(description = "응답 상태 코드", example = "200")
    private int status;

    @Schema(description = "응답 메시지", example = "요청이 성공적으로 처리되었습니다.")
    private String message;

    @Schema(description = "응답 데이터")
    private T data;

    /**
     * 성공 응답 생성 (데이터 포함)
     * 
     * @param data 응답 데이터
     * @param <T> 데이터 타입
     * @return 성공 응답
     */
    public static <T> ApiResponse<T> success(T data) {
        return ApiResponse.<T>builder()
                .status(200)
                .message("요청이 성공적으로 처리되었습니다.")
                .data(data)
                .build();
    }

    /**
     * 성공 응답 생성 (데이터 및 메시지 포함)
     * 
     * @param data 응답 데이터
     * @param message 응답 메시지
     * @param <T> 데이터 타입
     * @return 성공 응답
     */
    public static <T> ApiResponse<T> success(T data, String message) {
        return ApiResponse.<T>builder()
                .status(200)
                .message(message)
                .data(data)
                .build();
    }

    /**
     * 오류 응답 생성
     * 
     * @param status 오류 상태 코드
     * @param message 오류 메시지
     * @param <T> 데이터 타입
     * @return 오류 응답
     */
    public static <T> ApiResponse<T> error(int status, String message) {
        return ApiResponse.<T>builder()
                .status(status)
                .message(message)
                .data(null)
                .build();
    }
}
