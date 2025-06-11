package com.won.smarketing.content.domain.model;

import lombok.*;

import java.time.LocalDate;

/**
 * 콘텐츠 생성 조건 도메인 모델
 * AI 콘텐츠 생성 시 사용되는 조건 정보
 */
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
@Builder(toBuilder = true)
public class CreationConditions {

    /**
     * 홍보 대상 카테고리
     */
    private String category;

    /**
     * 특별 요구사항
     */
    private String requirement;

    /**
     * 톤앤매너
     */
    private String toneAndManner;

    /**
     * 감정 강도
     */
    private String emotionIntensity;

    /**
     * 이벤트명
     */
    private String eventName;

    /**
     * 홍보 시작일
     */
    private LocalDate startDate;

    /**
     * 홍보 종료일
     */
    private LocalDate endDate;

    /**
     * 사진 스타일 (포스터용)
     */
    private String photoStyle;
}
