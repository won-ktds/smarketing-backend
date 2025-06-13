package com.won.smarketing.store.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 메뉴 등록 요청 DTO
 * 메뉴 등록 시 필요한 정보를 전달합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "메뉴 등록 요청")
public class MenuCreateRequest {
    
    @Schema(description = "매장 ID", example = "1", required = true)
    @NotNull(message = "매장 ID는 필수입니다")
    private Long storeId;
    
    @Schema(description = "메뉴명", example = "아메리카노", required = true)
    @NotBlank(message = "메뉴명은 필수입니다")
    @Size(max = 100, message = "메뉴명은 100자 이하여야 합니다")
    private String menuName;
    
    @Schema(description = "카테고리", example = "커피")
    @Size(max = 50, message = "카테고리는 50자 이하여야 합니다")
    private String category;
    
    @Schema(description = "가격", example = "4500")
    @Min(value = 0, message = "가격은 0원 이상이어야 합니다")
    private Integer price;
    
    @Schema(description = "메뉴 설명", example = "진한 맛의 아메리카노")
    @Size(max = 500, message = "메뉴 설명은 500자 이하여야 합니다")
    private String description;
}



