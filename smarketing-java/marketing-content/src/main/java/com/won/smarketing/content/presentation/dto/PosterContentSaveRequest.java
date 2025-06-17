// smarketing-java/marketing-content/src/main/java/com/won/smarketing/content/presentation/dto/PosterContentSaveRequest.java
package com.won.smarketing.content.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.util.List;

/**
 * 포스터 콘텐츠 저장 요청 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "포스터 콘텐츠 저장 요청")
public class PosterContentSaveRequest {

//    @Schema(description = "콘텐츠 ID", example = "1", required = true)
//    @NotNull(message = "콘텐츠 ID는 필수입니다")
//    private Long contentId;

    @Schema(description = "매장 ID", example = "1", required = true)
    @NotNull(message = "매장 ID는 필수입니다")
    private Long storeId;

    @Schema(description = "제목", example = "특별 이벤트 안내")
    private String title;

    @Schema(description = "콘텐츠 내용")
    private String content;

    @Schema(description = "선택된 포스터 이미지 URL")
    private List<String> images;

    @Schema(description = "발행 상태", example = "PUBLISHED")
    private String status;

    // CreationConditions에 필요한 필드들
    @Schema(description = "콘텐츠 카테고리", example = "이벤트")
    private String category;

    @Schema(description = "구체적인 요구사항", example = "신메뉴 출시 이벤트 포스터를 만들어주세요")
    private String requirement;

    @Schema(description = "톤앤매너", example = "전문적")
    private String toneAndManner;

    @Schema(description = "감정 강도", example = "보통")
    private String emotionIntensity;

    @Schema(description = "이벤트명", example = "신메뉴 출시 이벤트")
    private String eventName;

    @Schema(description = "이벤트 시작일", example = "2024-01-15")
    private LocalDate startDate;

    @Schema(description = "이벤트 종료일", example = "2024-01-31")
    private LocalDate endDate;

    @Schema(description = "사진 스타일", example = "밝고 화사한")
    private String photoStyle;
}