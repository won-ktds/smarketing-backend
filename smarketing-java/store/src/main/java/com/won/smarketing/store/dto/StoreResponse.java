package com.won.smarketing.store.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.persistence.Column;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 매장 응답 DTO
 * 매장 정보를 클라이언트에게 전달합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "매장 응답")
public class StoreResponse {
    
    @Schema(description = "매장 ID", example = "1")
    private Long storeId;
    
    @Schema(description = "매장명", example = "맛있는 카페")
    private String storeName;

    @Schema(description = "업종", example = "카페")
    private String businessType;

    @Schema(description = "가게 사진")
    private String storeImage;

    @Schema(description = "주소", example = "서울시 강남구 테헤란로 123")
    private String address;

    @Schema(description = "전화번호", example = "02-1234-5678")
    private String phoneNumber;

    @Schema(description = "영업시간", example = "09:00 - 22:00")
    private String businessHours;

    @Schema(description = "휴무일", example = "매주 일요일")
    private String closedDays;

    @Schema(description = "좌석 수", example = "20")
    private Integer seatCount;

    @Schema(description = "SNS 계정 정보", example = "인스타그램: @mystore")
    private String snsAccounts;

    @Schema(description = "매장 설명", example = "따뜻한 분위기의 동네 카페입니다.")
    private String description;

    @Schema(description = "등록일시", example = "2024-01-15T10:30:00")
    private LocalDateTime createdAt;

    @Schema(description = "수정일시", example = "2024-01-15T10:30:00")
    private LocalDateTime updatedAt;
}

