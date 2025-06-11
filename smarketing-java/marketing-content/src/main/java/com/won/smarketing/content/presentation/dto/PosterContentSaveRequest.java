package com.won.smarketing.content.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 포스터 콘텐츠 저장 요청 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "포스터 콘텐츠 저장 요청")
public class PosterContentSaveRequest {

    @Schema(description = "콘텐츠 ID", example = "1", required = true)
    @NotNull(message = "콘텐츠 ID는 필수입니다")
    private Long contentId;

    @Schema(description = "최종 제목", example = "특별 이벤트 안내")
    private String finalTitle;

    @Schema(description = "최종 콘텐츠 내용")
    private String finalContent;

    @Schema(description = "선택된 포스터 이미지 URL")
    private String selectedPosterImage;

    @Schema(description = "발행 상태", example = "PUBLISHED")
    private String status;
}