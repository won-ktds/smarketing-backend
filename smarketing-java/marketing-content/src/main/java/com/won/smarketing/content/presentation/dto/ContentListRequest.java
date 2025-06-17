package com.won.smarketing.content.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 콘텐츠 목록 조회 요청 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "콘텐츠 목록 조회 요청")
public class ContentListRequest {

    @Schema(description = "콘텐츠 타입", example = "SNS_POST")
    private String contentType;

    @Schema(description = "플랫폼", example = "INSTAGRAM")
    private String platform;

    @Schema(description = "조회 기간", example = "7days")
    private String period;

    @Schema(description = "정렬 기준", example = "createdAt")
    private String sortBy;

    @Schema(description = "정렬 방향", example = "DESC")
    private String sortDirection;

    @Schema(description = "페이지 번호", example = "0")
    private Integer page;

    @Schema(description = "페이지 크기", example = "20")
    private Integer size;
}
