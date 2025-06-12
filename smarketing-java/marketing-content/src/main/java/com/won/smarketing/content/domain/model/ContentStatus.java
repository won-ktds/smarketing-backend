// marketing-content/src/main/java/com/won/smarketing/content/domain/model/ContentStatus.java
package com.won.smarketing.content.domain.model;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

/**
 * 콘텐츠 상태 열거형
 * Clean Architecture의 Domain Layer에 위치하는 비즈니스 규칙
 */
@Getter
@RequiredArgsConstructor
public enum ContentStatus {

    DRAFT("임시저장"),
    PUBLISHED("게시됨"),
    SCHEDULED("예약됨"),
    DELETED("삭제됨"),
    PROCESSING("처리중");

    private final String displayName;

    /**
     * 문자열로부터 ContentStatus 변환
     * @param value 문자열 값
     * @return ContentStatus enum
     * @throws IllegalArgumentException 유효하지 않은 값인 경우
     */
    public static ContentStatus fromString(String value) {
        if (value == null) {
            throw new IllegalArgumentException("ContentStatus 값은 null일 수 없습니다.");
        }

        try {
            return ContentStatus.valueOf(value.toUpperCase());
        } catch (IllegalArgumentException e) {
            throw new IllegalArgumentException("유효하지 않은 ContentStatus 값입니다: " + value);
        }
    }
}