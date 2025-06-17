package com.won.smarketing.common.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * 페이징 응답 DTO
 * 페이징된 데이터 응답에 사용되는 공통 형식
 * 
 * @param <T> 응답 데이터 타입
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "페이징 응답")
public class PageResponse<T> {

    @Schema(description = "페이지 컨텐츠", example = "[...]")
    private List<T> content;

    @Schema(description = "페이지 번호 (0부터 시작)", example = "0")
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

    /**
     * 성공적인 페이징 응답 생성
     * 
     * @param content 페이지 컨텐츠
     * @param pageNumber 페이지 번호
     * @param pageSize 페이지 크기
     * @param totalElements 전체 요소 수
     * @param <T> 데이터 타입
     * @return 페이징 응답
     */
    public static <T> PageResponse<T> of(List<T> content, int pageNumber, int pageSize, long totalElements) {
        int totalPages = (int) Math.ceil((double) totalElements / pageSize);
        
        return PageResponse.<T>builder()
                .content(content)
                .pageNumber(pageNumber)
                .pageSize(pageSize)
                .totalElements(totalElements)
                .totalPages(totalPages)
                .first(pageNumber == 0)
                .last(pageNumber >= totalPages - 1)
                .build();
    }
}
