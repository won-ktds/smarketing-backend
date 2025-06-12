// marketing-content/src/main/java/com/won/smarketing/content/domain/model/Platform.java
package com.won.smarketing.content.domain.model;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

/**
 * 플랫폼 열거형
 * Clean Architecture의 Domain Layer에 위치하는 비즈니스 규칙
 */
@Getter
@RequiredArgsConstructor
public enum Platform {

    INSTAGRAM("인스타그램"),
    NAVER_BLOG("네이버 블로그"),
    FACEBOOK("페이스북"),
    KAKAO_STORY("카카오스토리"),
    YOUTUBE("유튜브"),
    GENERAL("일반");

    private final String displayName;

    /**
     * 문자열로부터 Platform 변환
     * @param value 문자열 값
     * @return Platform enum
     * @throws IllegalArgumentException 유효하지 않은 값인 경우
     */
    public static Platform fromString(String value) {
        if (value == null) {
            throw new IllegalArgumentException("Platform 값은 null일 수 없습니다.");
        }

        try {
            return Platform.valueOf(value.toUpperCase());
        } catch (IllegalArgumentException e) {
            throw new IllegalArgumentException("유효하지 않은 Platform 값입니다: " + value);
        }
    }
}