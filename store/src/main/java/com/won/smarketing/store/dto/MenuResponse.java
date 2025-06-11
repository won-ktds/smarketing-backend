package com.won.smarketing.store.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 메뉴 정보 응답 DTO
 * 메뉴 정보 조회/등록/수정 시 반환되는 데이터
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "메뉴 정보 응답")
public class MenuResponse {

    @Schema(description = "메뉴 ID", example = "1")
    private Long menuId;

    @Schema(description = "메뉴명", example = "아메리카노")
    private String menuName;

    @Schema(description = "메뉴 카테고리", example = "커피")
    private String category;

    @Schema(description = "가격", example = "4500")
    private Integer price;

    @Schema(description = "메뉴 설명", example = "진한 원두의 깊은 맛")
    private String description;

    @Schema(description = "메뉴 이미지 URL", example = "https://example.com/americano.jpg")
    private String image;

    @Schema(description = "등록 시각")
    private LocalDateTime createdAt;

    @Schema(description = "수정 시각")
    private LocalDateTime updatedAt;
}
