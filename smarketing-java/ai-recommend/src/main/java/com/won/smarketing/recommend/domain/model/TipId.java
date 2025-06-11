package com.won.smarketing.recommend.domain.model;

import lombok.*;

/**
 * 마케팅 팁 식별자 값 객체
 * 마케팅 팁의 고유 식별자를 나타내는 도메인 객체
 */
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
@EqualsAndHashCode
public class TipId {

    private Long value;

    /**
     * TipId 생성 팩토리 메서드
     * 
     * @param value 식별자 값
     * @return TipId 인스턴스
     */
    public static TipId of(Long value) {
        if (value == null || value <= 0) {
            throw new IllegalArgumentException("TipId는 양수여야 합니다.");
        }
        return new TipId(value);
    }
}
