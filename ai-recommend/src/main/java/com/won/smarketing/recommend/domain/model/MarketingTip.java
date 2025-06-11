package com.won.smarketing.recommend.domain.model;

import lombok.*;

import java.time.LocalDateTime;

/**
 * 마케팅 팁 도메인 모델
 * AI가 생성한 마케팅 팁과 관련 정보를 관리
 */
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
@Builder
public class MarketingTip {

    /**
     * 마케팅 팁 고유 식별자
     */
    private TipId id;

    /**
     * 매장 ID
     */
    private Long storeId;

    /**
     * AI가 생성한 마케팅 팁 내용
     */
    private String tipContent;

    /**
     * 팁 생성 시 참고한 날씨 데이터
     */
    private WeatherData weatherData;

    /**
     * 팁 생성 시 참고한 매장 데이터
     */
    private StoreData storeData;

    /**
     * 팁 생성 시각
     */
    private LocalDateTime createdAt;

    /**
     * 팁 내용 업데이트
     *
     * @param newContent 새로운 팁 내용
     */
    public void updateContent(String newContent) {
        if (newContent == null || newContent.trim().isEmpty()) {
            throw new IllegalArgumentException("팁 내용은 비어있을 수 없습니다.");
        }
        this.tipContent = newContent.trim();
    }
}