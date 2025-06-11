package com.won.smarketing.content.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 콘텐츠 수정 요청 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "콘텐츠 수정 요청")
public class ContentUpdateRequest {

    @Schema(description = "제목", example = "수정된 제목")
    private String title;

    @Schema(description = "콘텐츠 내용")
    private String content;

    @Schema(description = "홍보 시작일")
    private LocalDateTime promotionStartDate;

    @Schema(description = "홍보 종료일")
    private LocalDateTime promotionEndDate;

    @Schema(description = "상태", example = "PUBLISHED")
    private String status;
}