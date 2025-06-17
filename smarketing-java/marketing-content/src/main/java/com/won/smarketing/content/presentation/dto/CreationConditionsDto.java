// marketing-content/src/main/java/com/won/smarketing/content/presentation/dto/CreationConditionsDto.java
package com.won.smarketing.content.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

/**
 * 콘텐츠 생성 조건 DTO
 */
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "콘텐츠 생성 조건")
public class CreationConditionsDto {

    @Schema(description = "카테고리", example = "음식")
    private String category;

    @Schema(description = "생성 요구사항", example = "젊은 고객층을 타겟으로 한 재미있는 콘텐츠")
    private String requirement;

    @Schema(description = "톤앤매너", example = "친근하고 활발한")
    private String toneAndManner;

    @Schema(description = "감정 강도", example = "보통")
    private String emotionIntensity;

    @Schema(description = "이벤트명", example = "신메뉴 출시 이벤트")
    private String eventName;

    @Schema(description = "시작일")
    private LocalDate startDate;

    @Schema(description = "종료일")
    private LocalDate endDate;

    @Schema(description = "사진 스타일", example = "모던하고 깔끔한")
    private String photoStyle;
}