package com.won.smarketing.content.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
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

    @Schema(description = "매장 ID", example = "1")
    private Long storeId;

    @Schema(description = "제목", example = "특별 이벤트 안내")
    private String title;

    @Schema(description = "콘텐츠 내용")
    private String content;

    @Schema(description = "선택된 포스터 이미지 URL")
    private List<String> images;

    @Schema(description = "콘텐츠 카테고리", example = "이벤트")
    private String category;

    @Schema(description = "구체적인 요구사항", example = "신메뉴 출시 이벤트 포스터를 만들어주세요")
    private String requirement;

    @Schema(description = "이벤트명", example = "신메뉴 출시 이벤트")
    private String eventName;

    @Schema(description = "이벤트 시작일", example = "2024-01-15")
    private LocalDate startDate;

    @Schema(description = "이벤트 종료일", example = "2024-01-31")
    private LocalDate endDate;

    @Schema(description = "사진 스타일", example = "밝고 화사한")
    private String photoStyle;
}