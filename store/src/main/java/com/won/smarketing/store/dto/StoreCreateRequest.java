package com.won.smarketing.store.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;
import javax.validation.constraints.Size;

/**
 * 매장 등록 요청 DTO
 * 매장 등록 시 필요한 정보를 담는 데이터 전송 객체
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "매장 등록 요청 정보")
public class StoreCreateRequest {

    @Schema(description = "매장 소유자 사용자 ID", example = "testuser", required = true)
    @NotBlank(message = "사용자 ID는 필수입니다.")
    private String userId;

    @Schema(description = "매장명", example = "맛있는 카페", required = true)
    @NotBlank(message = "매장명은 필수입니다.")
    @Size(max = 200, message = "매장명은 200자 이하여야 합니다.")
    private String storeName;

    @Schema(description = "매장 이미지 URL", example = "https://example.com/store.jpg")
    private String storeImage;

    @Schema(description = "업종", example = "카페", required = true)
    @NotBlank(message = "업종은 필수입니다.")
    @Size(max = 100, message = "업종은 100자 이하여야 합니다.")
    private String businessType;

    @Schema(description = "매장 주소", example = "서울시 강남구 테헤란로 123", required = true)
    @NotBlank(message = "주소는 필수입니다.")
    @Size(max = 500, message = "주소는 500자 이하여야 합니다.")
    private String address;

    @Schema(description = "매장 전화번호", example = "02-1234-5678", required = true)
    @NotBlank(message = "전화번호는 필수입니다.")
    @Pattern(regexp = "^\\d{2,3}-\\d{3,4}-\\d{4}$", message = "올바른 전화번호 형식이 아닙니다.")
    private String phoneNumber;

    @Schema(description = "사업자 번호", example = "123-45-67890", required = true)
    @NotBlank(message = "사업자 번호는 필수입니다.")
    @Pattern(regexp = "^\\d{3}-\\d{2}-\\d{5}$", message = "사업자 번호 형식이 올바르지 않습니다.")
    private String businessNumber;

    @Schema(description = "인스타그램 계정", example = "@mycafe")
    @Size(max = 100, message = "인스타그램 계정은 100자 이하여야 합니다.")
    private String instaAccount;

    @Schema(description = "네이버 블로그 계정", example = "mycafe_blog")
    @Size(max = 100, message = "네이버 블로그 계정은 100자 이하여야 합니다.")
    private String naverBlogAccount;

    @Schema(description = "오픈 시간", example = "09:00")
    @Pattern(regexp = "^\\d{2}:\\d{2}$", message = "올바른 시간 형식이 아닙니다. (HH:MM)")
    private String openTime;

    @Schema(description = "마감 시간", example = "22:00")
    @Pattern(regexp = "^\\d{2}:\\d{2}$", message = "올바른 시간 형식이 아닙니다. (HH:MM)")
    private String closeTime;

    @Schema(description = "휴무일", example = "매주 월요일")
    @Size(max = 100, message = "휴무일은 100자 이하여야 합니다.")
    private String closedDays;

    @Schema(description = "좌석 수", example = "20")
    private Integer seatCount;
}
