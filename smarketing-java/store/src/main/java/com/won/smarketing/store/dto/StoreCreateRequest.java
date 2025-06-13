package com.won.smarketing.store.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 매장 등록 요청 DTO
 * 매장 등록 시 필요한 정보를 전달합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "매장 등록 요청")
public class StoreCreateRequest {
    
    @Schema(description = "매장명", example = "맛있는 카페", required = true)
    @NotBlank(message = "매장명은 필수입니다")
    @Size(max = 100, message = "매장명은 100자 이하여야 합니다")
    private String storeName;
    
    @Schema(description = "업종", example = "카페")
    @Size(max = 50, message = "업종은 50자 이하여야 합니다")
    private String businessType;
    
    @Schema(description = "주소", example = "서울시 강남구 테헤란로 123", required = true)
    @NotBlank(message = "주소는 필수입니다")
    @Size(max = 200, message = "주소는 200자 이하여야 합니다")
    private String address;
    
    @Schema(description = "전화번호", example = "02-1234-5678")
    @Size(max = 20, message = "전화번호는 20자 이하여야 합니다")
    private String phoneNumber;
    
    @Schema(description = "영업시간", example = "09:00 - 22:00")
    @Size(max = 100, message = "영업시간은 100자 이하여야 합니다")
    private String businessHours;
    
    @Schema(description = "휴무일", example = "매주 일요일")
    @Size(max = 100, message = "휴무일은 100자 이하여야 합니다")
    private String closedDays;
    
    @Schema(description = "좌석 수", example = "20")
    private Integer seatCount;
    
    @Schema(description = "SNS 계정 정보", example = "인스타그램: @mystore")
    @Size(max = 500, message = "SNS 계정 정보는 500자 이하여야 합니다")
    private String snsAccounts;
    
    @Schema(description = "매장 설명", example = "따뜻한 분위기의 동네 카페입니다.")
    @Size(max = 1000, message = "매장 설명은 1000자 이하여야 합니다")
    private String description;
}


