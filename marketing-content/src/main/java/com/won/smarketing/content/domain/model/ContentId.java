package com.won.smarketing.content.domain.model;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * 콘텐츠 식별자 값 객체
 * 콘텐츠의 고유 식별자를 나타내는 도메인 객체
 */
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
@EqualsAndHashCode
public class ContentId {

    private Long value;

    /**
     * ContentId 생성 팩토리 메서드
     * 
     * @param value 식별자 값
     * @return ContentId 인스턴스
     */
    public static ContentId of(Long value) {
        if (value == null || value <= 0) {
            throw new IllegalArgumentException("ContentId는 양수여야 합니다.");
        }
        return new ContentId(value);
    }
}
