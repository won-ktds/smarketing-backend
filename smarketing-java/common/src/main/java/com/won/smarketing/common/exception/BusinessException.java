package com.won.smarketing.common.exception;

import lombok.Getter;

/**
 * 비즈니스 로직 예외
 * 애플리케이션 내 비즈니스 규칙 위반 시 발생하는 예외
 */
@Getter
public class BusinessException extends RuntimeException {

    private final ErrorCode errorCode;

    /**
     * 비즈니스 예외 생성자
     * 
     * @param errorCode 오류 코드
     */
    public BusinessException(ErrorCode errorCode) {
        super(errorCode.getMessage());
        this.errorCode = errorCode;
    }

    /**
     * 비즈니스 예외 생성자 (추가 메시지 포함)
     * 
     * @param errorCode 오류 코드
     * @param message 추가 메시지
     */
    public BusinessException(ErrorCode errorCode, String message) {
        super(message);
        this.errorCode = errorCode;
    }
}
