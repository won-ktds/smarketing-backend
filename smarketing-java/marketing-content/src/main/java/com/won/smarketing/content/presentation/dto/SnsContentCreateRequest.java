package com.won.smarketing.content.presentation.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.util.List;

/**
 * SNS 콘텐츠 생성 요청 DTO
 *
 * AI 기반 SNS 콘텐츠 생성을 위한 요청 정보를 담고 있습니다.
 * 사용자가 입력한 생성 조건을 바탕으로 AI가 적절한 SNS 콘텐츠를 생성합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "SNS 콘텐츠 생성 요청")
@JsonIgnoreProperties(ignoreUnknown = true)
public class SnsContentCreateRequest {

    // ==================== 기본 정보 ====================

    @Schema(description = "매장 ID", example = "1", required = true)
    @NotNull(message = "매장 ID는 필수입니다")
    private Long storeId;

    @Schema(description = "매장 이름", example = "명륜진사갈비")
    private String storeName;

    @Schema(description = "업종", example = "한식")
    private String storeType;
    
    @Schema(description = "대상 플랫폼",
            example = "INSTAGRAM",
            allowableValues = {"INSTAGRAM", "NAVER_BLOG", "FACEBOOK", "KAKAO_STORY"},
            required = true)
    @NotBlank(message = "플랫폼은 필수입니다")
    private String platform;

    @Schema(description = "콘텐츠 제목", example = "1", required = true)
    @NotNull(message = "콘텐츠 제목은 필수입니다")
    private String title;

    // ==================== 콘텐츠 생성 조건 ====================

    @Schema(description = "콘텐츠 카테고리",
            example = "메뉴소개",
            allowableValues = {"메뉴소개", "이벤트", "일상", "인테리어", "고객후기", "기타"})
    private String category;

    @Schema(description = "구체적인 요구사항 또는 홍보하고 싶은 내용",
            example = "새로 출시된 시그니처 버거를 홍보하고 싶어요")
    @Size(max = 500, message = "요구사항은 500자 이하로 입력해주세요")
    private String requirement;

    @Schema(description = "타겟층", example = "10대 청소년")
    private String target;

    @Schema(description = "콘텐츠 타입", example = "SNS 게시물")
    private String contentType;

//    @Schema(description = "톤앤매너",
//            example = "친근함",
//            allowableValues = {"친근함", "전문적", "유머러스", "감성적", "트렌디"})
//    private String toneAndManner;

//    @Schema(description = "감정 강도",
//            example = "보통",
//            allowableValues = {"약함", "보통", "강함"})
//    private String emotionIntensity;

    // ==================== 이벤트 정보 ====================

    @Schema(description = "이벤트명 (이벤트 콘텐츠인 경우)",
            example = "신메뉴 출시 이벤트")
    @Size(max = 200, message = "이벤트명은 200자 이하로 입력해주세요")
    private String eventName;

    @Schema(description = "이벤트 시작일 (이벤트 콘텐츠인 경우)",
            example = "2024-01-15")
    private LocalDate startDate;

    @Schema(description = "이벤트 종료일 (이벤트 콘텐츠인 경우)",
            example = "2024-01-31")
    private LocalDate endDate;

    // ==================== 미디어 정보 ====================

    @Schema(description = "업로드된 이미지 파일 경로 목록")
    private List<String> images;

    @Schema(description = "사진 스타일 선호도",
            example = "밝고 화사한",
            allowableValues = {"밝고 화사한", "차분하고 세련된", "빈티지한", "모던한", "자연스러운"})
    private String photoStyle;

    // ==================== 추가 옵션 ====================

    @Schema(description = "해시태그 포함 여부", example = "true")
    @Builder.Default
    private Boolean includeHashtags = true;

    @Schema(description = "이모지 포함 여부", example = "true")
    @Builder.Default
    private Boolean includeEmojis = true;

    @Schema(description = "콜투액션 포함 여부 (좋아요, 팔로우 요청 등)", example = "true")
    @Builder.Default
    private Boolean includeCallToAction = true;

    @Schema(description = "매장 위치 정보 포함 여부", example = "false")
    @Builder.Default
    private Boolean includeLocation = false;

    // ==================== 플랫폼별 옵션 ====================

    @Schema(description = "인스타그램 스토리용 여부 (Instagram인 경우)", example = "false")
    @Builder.Default
    private Boolean forInstagramStory = false;

    @Schema(description = "네이버 블로그 포스팅용 여부 (Naver Blog인 경우)", example = "false")
    @Builder.Default
    private Boolean forNaverBlogPost = false;

    // ==================== AI 생성 옵션 ====================

    @Schema(description = "대안 제목 생성 개수", example = "3")
    @Builder.Default
    private Integer alternativeTitleCount = 3;

    @Schema(description = "대안 해시태그 세트 생성 개수", example = "2")
    @Builder.Default
    private Integer alternativeHashtagSetCount = 2;

    @Schema(description = "AI 모델 버전 지정 (없으면 기본값 사용)", example = "gpt-4-turbo")
    private String preferredAiModel;

    // ==================== 검증 메서드 ====================

    /**
     * 이벤트 날짜 유효성 검증
     * 시작일이 종료일보다 이후인지 확인
     */
    public boolean isValidEventDates() {
        if (startDate != null && endDate != null) {
            return !startDate.isAfter(endDate);
        }
        return true;
    }

    /**
     * 플랫폼별 필수 조건 검증
     */
    public boolean isValidForPlatform() {
        if ("INSTAGRAM".equals(platform)) {
            // 인스타그램은 이미지가 권장됨
            return images != null && !images.isEmpty();
        }
        if ("NAVER_BLOG".equals(platform)) {
            // 네이버 블로그는 상세한 내용이 필요
            return requirement != null && requirement.length() >= 20;
        }
        return true;
    }
}
