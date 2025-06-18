// marketing-content/src/main/java/com/won/smarketing/content/domain/model/CreationConditions.java
package com.won.smarketing.content.domain.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

/**
 * 콘텐츠 생성 조건 도메인 모델
 * Clean Architecture의 Domain Layer에 위치하는 값 객체
 *
 * JPA 애노테이션을 제거하여 순수 도메인 모델로 유지
 * Infrastructure Layer의 JPA 엔티티는 별도로 관리
 */
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CreationConditions {

    private String id;
    private String category;
    private String requirement;
    private String storeName;
    private String storeType;
    private String target;
    private String eventName;
    private LocalDate startDate;
    private LocalDate endDate;
    private String photoStyle;
    private String promotionType;

    public CreationConditions(String category, String requirement, String toneAndManner, String emotionIntensity, String eventName, LocalDate startDate, LocalDate endDate, String photoStyle, String promotionType) {
    }

    /**
     * 이벤트 기간 유효성 검증
     * @return 시작일이 종료일보다 이전이거나 같으면 true
     */
    public boolean isValidEventPeriod() {
        if (startDate == null || endDate == null) {
            return true;
        }
        return !startDate.isAfter(endDate);
    }

    /**
     * 이벤트 조건 유무 확인
     * @return 이벤트명이나 날짜가 설정되어 있으면 true
     */
    public boolean hasEventInfo() {
        return eventName != null && !eventName.trim().isEmpty()
                || startDate != null
                || endDate != null;
    }
}