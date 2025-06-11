package com.won.smarketing.content.presentation.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

/**
 * SNS 콘텐츠 저장 요청 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "SNS 콘텐츠 저장 요청")
public class SnsContentSaveRequest {

    @Schema(description = "콘텐츠 ID", example = "1", required = true)
    @NotNull(message = "콘텐츠 ID는 필수입니다")
    private Long contentId;

    @Schema(description = "최종 제목", example = "맛있는 신메뉴를 소개합니다!")
    private String finalTitle;

    @Schema(description = "최종 콘텐츠 내용")
    private String finalContent;

    @Schema(description = "발행 상태", example = "PUBLISHED")
    private String status;
}