package com.won.smarketing.recommend.domain.model;

import lombok.*;

/**
 * 매장 데이터 값 객체
 * 마케팅 팁 생성에 사용되는 매장 정보
 */
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
@Builder
@EqualsAndHashCode
public class StoreData {

    /**
     * 매장명
     */
    private String storeName;

    /**
     * 업종
     */
    private String businessType;

    /**
     * 매장 위치 (주소)
     */
    private String location;

    /**
     * 매장 데이터 유효성 검증
     * 
     * @return 유효성 여부
     */
    public boolean isValid() {
        return storeName != null && !storeName.trim().isEmpty() &&
               businessType != null && !businessType.trim().isEmpty() &&
               location != null && !location.trim().isEmpty();
    }

    /**
     * 업종 카테고리 분류
     * 
     * @return 업종 카테고리
     */
    public String getBusinessCategory() {
        if (businessType == null) {
            return "기타";
        }
        
        String lowerCaseType = businessType.toLowerCase();
        
        if (lowerCaseType.contains("카페") || lowerCaseType.contains("커피")) {
            return "카페";
        } else if (lowerCaseType.contains("식당") || lowerCaseType.contains("레스토랑")) {
            return "음식점";
        } else if (lowerCaseType.contains("베이커리") || lowerCaseType.contains("빵")) {
            return "베이커리";
        } else if (lowerCaseType.contains("치킨") || lowerCaseType.contains("피자")) {
            return "패스트푸드";
        } else {
            return "기타";
        }
    }
}
