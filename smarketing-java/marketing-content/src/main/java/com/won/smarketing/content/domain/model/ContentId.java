// marketing-content/src/main/java/com/won/smarketing/content/domain/model/ContentId.java
package com.won.smarketing.content.domain.model;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

/**
 * 콘텐츠 ID 값 객체
 * Clean Architecture의 Domain Layer에서 식별자를 타입 안전하게 관리
 */
@Getter
@RequiredArgsConstructor
@EqualsAndHashCode
public class ContentId {

    private final Long value;

    /**
     * Long 값으로부터 ContentId 생성
     * @param value ID 값
     * @return ContentId 인스턴스
     */
    public static ContentId of(Long value) {
        if (value == null || value <= 0) {
            throw new IllegalArgumentException("ContentId는 양수여야 합니다.");
        }
        return new ContentId(value);
    }

    /**
     * 새로운 ContentId 생성 (ID가 없는 경우)
     * @return null 값을 가진 ContentId
     */
    public static ContentId newId() {
        return new ContentId(null);
    }

    /**
     * ID 값 존재 여부 확인
     * @return ID가 null이 아니면 true
     */
    public boolean hasValue() {
        return value != null;
    }

    @Override
    public String toString() {
        return "ContentId{" + "value=" + value + '}';
    }
}