package com.won.smarketing.content.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 콘텐츠 재생성 요청 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "콘텐츠 재생성 요청")
public class ContentRegenerateRequest {

    @Schema(description = "원본 콘텐츠 ID", example = "1", required = true)
    @NotNull(message = "원본 콘텐츠 ID는 필수입니다")
    private Long originalContentId;

    @Schema(description = "수정된 톤앤매너", example = "전문적")
    private String toneAndManner;

    @Schema(description = "수정된 프로모션 유형", example = "신메뉴 알림")
    private String promotionType;

    @Schema(description = "수정된 감정 강도", example = "열정적")
    private String emotionIntensity;

    @Schema(description = "추가 요구사항", example = "더 감성적으로 작성해주세요")
    private String additionalRequirements;
}
