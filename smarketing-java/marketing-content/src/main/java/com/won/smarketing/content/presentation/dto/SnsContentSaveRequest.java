// smarketing-java/marketing-content/src/main/java/com/won/smarketing/content/presentation/dto/SnsContentSaveRequest.java
package com.won.smarketing.content.presentation.dto;

import com.won.smarketing.content.domain.model.ContentType;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
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

//    @Schema(description = "콘텐츠 ID", example = "1", required = true)
//    @NotNull(message = "콘텐츠 ID는 필수입니다")
//    private Long contentId;

    @Schema(description = "매장 ID", example = "1", required = true)
    @NotNull(message = "매장 ID는 필수입니다")
    private Long storeId;

    @Schema(description = "콘텐트 타입", example = "1", required = true)
    @NotNull(message = "콘텐트 타입은 필수입니다")
    private ContentType contentType;
    
    @Schema(description = "플랫폼", example = "INSTAGRAM", required = true)
    @NotBlank(message = "플랫폼은 필수입니다")
    private String platform;

    @Schema(description = "제목", example = "맛있는 신메뉴를 소개합니다!")
    private String title;

    @Schema(description = "콘텐츠 내용")
    private String content;

    @Schema(description = "해시태그 목록")
    private List<String> hashtags;

    @Schema(description = "이미지 URL 목록")
    private List<String> images;

    @Schema(description = "최종 제목", example = "맛있는 신메뉴를 소개합니다!")
    private String finalTitle;

    @Schema(description = "최종 콘텐츠 내용")
    private String finalContent;

    @Schema(description = "발행 상태", example = "PUBLISHED")
    private String status;

    // CreationConditions에 필요한 필드들
    @Schema(description = "콘텐츠 카테고리", example = "메뉴소개")
    private String category;

    @Schema(description = "구체적인 요구사항", example = "새로 출시된 시그니처 버거를 홍보하고 싶어요")
    private String requirement;

    @Schema(description = "톤앤매너", example = "친근함")
    private String toneAndManner;

    @Schema(description = "감정 강도", example = "보통")
    private String emotionIntensity;

    @Schema(description = "이벤트명", example = "신메뉴 출시 이벤트")
    private String eventName;

    @Schema(description = "이벤트 시작일", example = "2024-01-15")
    private LocalDate startDate;

    @Schema(description = "이벤트 종료일", example = "2024-01-31")
    private LocalDate endDate;
}