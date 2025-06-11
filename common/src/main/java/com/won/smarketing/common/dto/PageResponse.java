package com.won.smarketing.common.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * 페이지네이션 응답 DTO
 * 페이지 단위 조회 결과를 담는 공통 형식
 * 
 * @param <T> 페이지 내용의 데이터 타입
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "페이지네이션 응답")
public class PageResponse<T> {

    @Schema(description = "페이지 내용")
    private List<T> content;

    @Schema(description = "현재 페이지 번호", example = "0")
    private int pageNumber;

    @Schema(description = "페이지 크기", example = "20")
    private int pageSize;

    @Schema(description = "전체 요소 수", example = "100")
    private long totalElements;

    @Schema(description = "전체 페이지 수", example = "5")
    private int totalPages;

    @Schema(description = "첫 번째 페이지 여부", example = "true")
    private boolean first;

    @Schema(description = "마지막 페이지 여부", example = "false")
    private boolean last;
}
