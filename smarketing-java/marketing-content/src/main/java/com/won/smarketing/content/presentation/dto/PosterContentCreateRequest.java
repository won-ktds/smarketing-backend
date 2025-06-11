package com.won.smarketing.content.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

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

    @Schema(description = "홍보 대상", example = "메뉴", required = true)
    @NotBlank(message = "홍보 대상은 필수입니다")
    private String targetAudience;

    @Schema(description = "홍보 시작일", required = true)
    @NotNull(message = "홍보 시작일은 필수입니다")
    private LocalDateTime promotionStartDate;

    @Schema(description = "홍보 종료일", required = true)
    @NotNull(message = "홍보 종료일은 필수입니다")
    private LocalDateTime promotionEndDate;

    @Schema(description = "이벤트명 (이벤트 홍보시)", example = "신메뉴 출시 이벤트")
    private String eventName;

    @Schema(description = "이미지 스타일", example = "모던")
    private String imageStyle;

    @Schema(description = "프로모션 유형", example = "할인 정보")
    private String promotionType;

    @Schema(description = "감정 강도", example = "보통")
    private String emotionIntensity;

    @Schema(description = "업로드된 이미지 URL 목록", required = true)
    @NotNull(message = "이미지는 1개 이상 필수입니다")
    @Size(min = 1, message = "이미지는 1개 이상 업로드해야 합니다")
    private List<String> images;
}