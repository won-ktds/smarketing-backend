// marketing-content/src/main/java/com/won/smarketing/content/domain/model/ContentId.java
package com.won.smarketing.content.domain.model;

import jakarta.persistence.Embeddable;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.util.Objects;

/**
 * 콘텐츠 ID 값 객체
 * Clean Architecture의 Domain Layer에 위치하는 식별자
 */
@Embeddable
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class ContentId {

    private Long value;

    /**
     * ContentId 생성 팩토리 메서드
     * @param value ID 값
     * @return ContentId 인스턴스
     */
    public static ContentId of(Long value) {
        if (value == null || value <= 0) {
            throw new IllegalArgumentException("ContentId 값은 양수여야 합니다.");
        }
        return new ContentId(value);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        ContentId contentId = (ContentId) o;
        return Objects.equals(value, contentId.value);
    }

    @Override
    public int hashCode() {
        return Objects.hash(value);
    }

    @Override
    public String toString() {
        return "ContentId{" + value + '}';
    }
}