// smarketing-java/marketing-content/src/main/java/com/won/smarketing/content/presentation/dto/PosterContentCreateRequest.java
package com.won.smarketing.content.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

/**
 * 포스터 콘텐츠 생성 요청 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "포스터 콘텐츠 생성 요청")
public class PosterContentCreateRequest {

    @Schema(description = "매장 ID", example = "1", required = true)
    @NotNull(message = "매장 ID는 필수입니다")
    private Long storeId;

    @Schema(description = "제목", example = "특별 이벤트 안내")
    private String title;

    @Schema(description = "홍보 대상", example = "메뉴", required = true)
    @NotBlank(message = "홍보 대상은 필수입니다")
    private String targetAudience;

    @Schema(description = "홍보 시작일", required = true)
    @NotNull(message = "홍보 시작일은 필수입니다")
    private LocalDateTime promotionStartDate;

    @Schema(description = "홍보 종료일", required = true)
    @NotNull(message = "홍보 종료일은 필수입니다")
    private LocalDateTime promotionEndDate;

    @Schema(description = "메뉴명 (메뉴 홍보시)", example = "카페라떼")
    private String menuName;

    @Schema(description = "이벤트명 (이벤트 홍보시)", example = "신메뉴 출시 이벤트")
    private String eventName;

    @Schema(description = "이미지 스타일", example = "모던")
    private String imageStyle;

    @Schema(description = "업로드된 이미지 URL 목록")
    private List<String> images;

    @Schema(description = "콘텐츠 카테고리", example = "이벤트")
    private String category;

    @Schema(description = "구체적인 요구사항", example = "신메뉴 출시 이벤트 포스터를 만들어주세요")
    private String requirement;

    @Schema(description = "이벤트 시작일", example = "2024-01-15")
    private LocalDate startDate;

    @Schema(description = "이벤트 종료일", example = "2024-01-31")
    private LocalDate endDate;

    @Schema(description = "사진 스타일", example = "밝고 화사한")
    private String photoStyle;

}