package com.won.smarketing.content.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;
import java.util.Map;

/**
 * 포스터 콘텐츠 생성 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "포스터 콘텐츠 생성 응답")
public class PosterContentCreateResponse {

    @Schema(description = "콘텐츠 ID", example = "1")
    private Long contentId;

    @Schema(description = "생성된 포스터 제목", example = "특별 이벤트 안내")
    private String title;

    @Schema(description = "생성된 포스터 텍스트 내용")
    private String content;

    @Schema(description = "생성된 포스터 타입")
    private String contentType;

    @Schema(description = "포스터 이미지 URL")
    private String posterImage;

    @Schema(description = "원본 이미지 URL 목록")
    private List<String> originalImages;

    @Schema(description = "이미지 스타일", example = "모던")
    private String imageStyle;

    @Schema(description = "생성 상태", example = "DRAFT")
    private String status;
    
    @Schema(description = "포스터사이즈", example = "800x600")
    private Map<String, String> posterSizes;
    
}