package com.won.smarketing.recommend.domain.event;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MarketingTipRequestEvent {

    private String requestId;           // 요청 고유 ID
    private Long userId;                // 사용자 ID
    private Long storeId;               // 매장 ID
    private String storeName;           // 매장명
    private String businessType;        // 업종
    private String location;            // 위치
    private Integer seatCount;          // 좌석 수
    private String menuData;            // 메뉴 데이터 (JSON)
    private LocalDateTime requestedAt;  // 요청 시각
    private Integer retryCount;         // 재시도 횟수
}