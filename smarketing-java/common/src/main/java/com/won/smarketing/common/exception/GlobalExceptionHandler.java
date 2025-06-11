package com.won.smarketing.common.exception;

import com.won.smarketing.common.dto.ApiResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.HashMap;
import java.util.Map;

/**
 * 전역 예외 처리기
 * 애플리케이션 전반의 예외를 통일된 형식으로 처리
 */
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * 비즈니스 예외 처리
     * 
     * @param ex 비즈니스 예외
     * @return 오류 응답
     */
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ApiResponse<Void>> handleBusinessException(BusinessException ex) {
        log.warn("Business exception occurred: {}", ex.getMessage());
        
        return ResponseEntity
                .status(ex.getErrorCode().getHttpStatus())
                .body(ApiResponse.error(
                        ex.getErrorCode().getHttpStatus().value(),
                        ex.getMessage()
                ));
    }

    /**
     * 입력값 검증 예외 처리
     * 
     * @param ex 입력값 검증 예외
     * @return 오류 응답
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ApiResponse<Map<String, String>>> handleValidationException(
            MethodArgumentNotValidException ex) {
        log.warn("Validation exception occurred: {}", ex.getMessage());
        
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getAllErrors().forEach(error -> {
            String fieldName = ((FieldError) error).getField();
            String errorMessage = error.getDefaultMessage();
            errors.put(fieldName, errorMessage);
        });

        return ResponseEntity.badRequest()
                .body(ApiResponse.<Map<String, String>>builder()
                        .status(400)
                        .message("입력값 검증에 실패했습니다.")
                        .data(errors)
                        .build());
    }

    /**
     * 일반적인 예외 처리
     * 
     * @param ex 예외
     * @return 오류 응답
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ApiResponse<Void>> handleException(Exception ex) {
        log.error("Unexpected exception occurred", ex);
        
        return ResponseEntity.internalServerError()
                .body(ApiResponse.error(500, "서버 내부 오류가 발생했습니다."));
    }
}
