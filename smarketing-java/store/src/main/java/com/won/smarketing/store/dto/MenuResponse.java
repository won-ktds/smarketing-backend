package com.won.smarketing.store.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 메뉴 응답 DTO
 * 메뉴 정보를 클라이언트에게 전달합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "메뉴 응답")
public class MenuResponse {
    
    @Schema(description = "메뉴 ID", example = "1")
    private Long menuId;
    
    @Schema(description = "매장 ID", example = "1")
    private Long storeId;
    
    @Schema(description = "메뉴명", example = "아메리카노")
    private String menuName;
    
    @Schema(description = "카테고리", example = "커피")
    private String category;
    
    @Schema(description = "가격", example = "4500")
    private Integer price;
    
    @Schema(description = "메뉴 설명", example = "진한 맛의 아메리카노")
    private String description;
    
    @Schema(description = "이미지 URL", example = "https://example.com/americano.jpg")
    private String image;
    
    @Schema(description = "등록일시", example = "2024-01-15T10:30:00")
    private LocalDateTime createdAt;
    
    @Schema(description = "수정일시", example = "2024-01-15T10:30:00")
    private LocalDateTime updatedAt;
}

