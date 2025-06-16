package com.won.smarketing.common.exception;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;

/**
 * 애플리케이션 오류 코드 정의
 * 각 오류 상황에 대한 코드, HTTP 상태, 메시지 정의
 */
@Getter
@RequiredArgsConstructor
public enum ErrorCode {

    // 회원 관련 오류
    MEMBER_NOT_FOUND(HttpStatus.NOT_FOUND, "M001", "회원을 찾을 수 없습니다."),
    DUPLICATE_MEMBER_ID(HttpStatus.BAD_REQUEST, "M002", "이미 사용 중인 사용자 ID입니다."),
    DUPLICATE_EMAIL(HttpStatus.BAD_REQUEST, "M003", "이미 사용 중인 이메일입니다."),
    DUPLICATE_BUSINESS_NUMBER(HttpStatus.BAD_REQUEST, "M004", "이미 등록된 사업자 번호입니다."),
    INVALID_PASSWORD(HttpStatus.BAD_REQUEST, "M005", "잘못된 패스워드입니다."),
    INVALID_TOKEN(HttpStatus.UNAUTHORIZED, "M006", "유효하지 않은 토큰입니다."),
    TOKEN_EXPIRED(HttpStatus.UNAUTHORIZED, "M007", "만료된 토큰입니다."),

    // 매장 관련 오류
    STORE_NOT_FOUND(HttpStatus.NOT_FOUND, "S001", "매장을 찾을 수 없습니다."),
    STORE_ALREADY_EXISTS(HttpStatus.BAD_REQUEST, "S002", "이미 등록된 매장이 있습니다."),
    MENU_NOT_FOUND(HttpStatus.NOT_FOUND, "S003", "메뉴를 찾을 수 없습니다."),

    // 마케팅 콘텐츠 관련 오류
    CONTENT_NOT_FOUND(HttpStatus.NOT_FOUND, "C001", "콘텐츠를 찾을 수 없습니다."),
    CONTENT_GENERATION_FAILED(HttpStatus.INTERNAL_SERVER_ERROR, "C002", "콘텐츠 생성에 실패했습니다."),
    AI_SERVICE_UNAVAILABLE(HttpStatus.SERVICE_UNAVAILABLE, "C003", "AI 서비스를 사용할 수 없습니다."),

    // AI 추천 관련 오류
    RECOMMENDATION_FAILED(HttpStatus.INTERNAL_SERVER_ERROR, "R001", "추천 생성에 실패했습니다."),
    EXTERNAL_API_ERROR(HttpStatus.SERVICE_UNAVAILABLE, "R002", "외부 API 호출에 실패했습니다."),

    FILE_NOT_FOUND(HttpStatus.NOT_FOUND, "F001", "파일을 찾을 수 없습니다."),
    FILE_UPLOAD_FAILED(HttpStatus.INTERNAL_SERVER_ERROR, "F002", "파일 업로드에 실패했습니다."),
    FILE_SIZE_EXCEEDED(HttpStatus.NOT_FOUND, "F003", "파일 크기가 제한을 초과했습니다."),
    INVALID_FILE_EXTENSION(HttpStatus.NOT_FOUND, "F004", "지원하지 않는 파일 확장자입니다."),
    INVALID_FILE_TYPE(HttpStatus.NOT_FOUND, "F005", "지원하지 않는 파일 형식입니다."),
    INVALID_FILE_NAME(HttpStatus.NOT_FOUND, "F006", "잘못된 파일명입니다."),
    INVALID_FILE_URL(HttpStatus.NOT_FOUND, "F007", "잘못된 파일 URL입니다."),
    STORAGE_CONTAINER_ERROR(HttpStatus.INTERNAL_SERVER_ERROR, "F008", "스토리지 컨테이너 오류가 발생했습니다."),

    // 공통 오류
    INTERNAL_SERVER_ERROR(HttpStatus.INTERNAL_SERVER_ERROR, "G001", "서버 내부 오류가 발생했습니다."),
    INVALID_INPUT_VALUE(HttpStatus.BAD_REQUEST, "G002", "잘못된 입력값입니다."),
    INVALID_TYPE_VALUE(HttpStatus.BAD_REQUEST, "G003", "잘못된 타입의 값입니다."),
    MISSING_REQUEST_PARAMETER(HttpStatus.BAD_REQUEST, "G004", "필수 요청 파라미터가 누락되었습니다."),
    ACCESS_DENIED(HttpStatus.FORBIDDEN, "G005", "접근이 거부되었습니다."),
    METHOD_NOT_ALLOWED(HttpStatus.METHOD_NOT_ALLOWED, "G006", "허용되지 않은 HTTP 메서드입니다.");

    private final HttpStatus httpStatus;
    private final String code;
    private final String message;
}
