package com.won.smarketing.recommend.domain.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * 매장 데이터 값 객체
 */
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class StoreData {
    private String storeName;
    private String businessType;
    private String location;
}
