package com.won.smarketing.store.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 매장 정보 응답 DTO
 * 매장 정보 조회/등록/수정 시 반환되는 데이터
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "매장 정보 응답")
public class StoreResponse {

    @Schema(description = "매장 ID", example = "1")
    private Long storeId;

    @Schema(description = "매장명", example = "맛있는 카페")
    private String storeName;

    @Schema(description = "매장 이미지 URL", example = "https://example.com/store.jpg")
    private String storeImage;

    @Schema(description = "업종", example = "카페")
    private String businessType;

    @Schema(description = "매장 주소", example = "서울시 강남구 테헤란로 123")
    private String address;

    @Schema(description = "매장 전화번호", example = "02-1234-5678")
    private String phoneNumber;

    @Schema(description = "사업자 번호", example = "123-45-67890")
    private String businessNumber;

    @Schema(description = "인스타그램 계정", example = "@mycafe")
    private String instaAccount;

    @Schema(description = "네이버 블로그 계정", example = "mycafe_blog")
    private String naverBlogAccount;

    @Schema(description = "오픈 시간", example = "09:00")
    private String openTime;

    @Schema(description = "마감 시간", example = "22:00")
    private String closeTime;

    @Schema(description = "휴무일", example = "매주 월요일")
    private String closedDays;

    @Schema(description = "좌석 수", example = "20")
    private Integer seatCount;

    @Schema(description = "등록 시각")
    private LocalDateTime createdAt;

    @Schema(description = "수정 시각")
    private LocalDateTime updatedAt;
}
