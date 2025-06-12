// marketing-content/src/main/java/com/won/smarketing/content/domain/model/ContentType.java
package com.won.smarketing.content.domain.model;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

/**
 * 콘텐츠 타입 열거형
 * Clean Architecture의 Domain Layer에 위치하는 비즈니스 규칙
 */
@Getter
@RequiredArgsConstructor
public enum ContentType {

    SNS("SNS 게시물"),
    POSTER("홍보 포스터"),
    VIDEO("동영상"),
    BLOG("블로그 포스트");

    private final String displayName;

    /**
     * 문자열로부터 ContentType 변환
     * @param value 문자열 값
     * @return ContentType enum
     * @throws IllegalArgumentException 유효하지 않은 값인 경우
     */
    public static ContentType fromString(String value) {
        if (value == null) {
            throw new IllegalArgumentException("ContentType 값은 null일 수 없습니다.");
        }

        try {
            return ContentType.valueOf(value.toUpperCase());
        } catch (IllegalArgumentException e) {
            throw new IllegalArgumentException("유효하지 않은 ContentType 값입니다: " + value);
        }
    }
}