package com.won.smarketing.recommend.domain.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * 메뉴 데이터 값 객체
 */
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MenuData {
    private Long menuId;
    private String menuName;
    private String category;
    private Integer price;
    private String description;
}
