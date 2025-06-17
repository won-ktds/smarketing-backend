package com.won.smarketing.content.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 콘텐츠 수정 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "콘텐츠 수정 응답")
public class ContentUpdateResponse {

    @Schema(description = "콘텐츠 ID", example = "1")
    private Long contentId;

    @Schema(description = "수정된 제목", example = "수정된 제목")
    private String title;

    @Schema(description = "수정된 콘텐츠 내용")
    private String content;

    @Schema(description = "상태", example = "PUBLISHED")
    private String status;

    @Schema(description = "수정일시")
    private LocalDateTime updatedAt;
}