package com.won.smarketing.recommend.domain.model;

import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * 팁 ID 값 객체
 */
@Getter
@EqualsAndHashCode
@NoArgsConstructor
@AllArgsConstructor
public class TipId {
    private Long value;

    public static TipId of(Long value) {
        return new TipId(value);
    }
}