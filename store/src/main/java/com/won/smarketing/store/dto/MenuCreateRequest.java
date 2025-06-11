package com.won.smarketing.store.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.validation.constraints.Min;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

/**
 * 메뉴 등록 요청 DTO
 * 메뉴 등록 시 필요한 정보를 담는 데이터 전송 객체
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "메뉴 등록 요청 정보")
public class MenuCreateRequest {

    @Schema(description = "매장 ID", example = "1", required = true)
    @NotNull(message = "매장 ID는 필수입니다.")
    private Long storeId;

    @Schema(description = "메뉴명", example = "아메리카노", required = true)
    @NotBlank(message = "메뉴명은 필수입니다.")
    @Size(max = 200, message = "메뉴명은 200자 이하여야 합니다.")
    private String menuName;

    @Schema(description = "메뉴 카테고리", example = "커피", required = true)
    @NotBlank(message = "카테고리는 필수입니다.")
    @Size(max = 100, message = "카테고리는 100자 이하여야 합니다.")
    private String category;

    @Schema(description = "가격", example = "4500", required = true)
    @NotNull(message = "가격은 필수입니다.")
    @Min(value = 0, message = "가격은 0 이상이어야 합니다.")
    private Integer price;

    @Schema(description = "메뉴 설명", example = "진한 원두의 깊은 맛")
    private String description;

    @Schema(description = "메뉴 이미지 URL", example = "https://example.com/americano.jpg")
    private String image;
}
