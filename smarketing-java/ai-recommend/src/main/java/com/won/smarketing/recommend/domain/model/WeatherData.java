package com.won.smarketing.recommend.domain.model;

import lombok.*;

/**
 * 날씨 데이터 값 객체
 * 마케팅 팁 생성에 사용되는 날씨 정보
 */
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
@Builder
@EqualsAndHashCode
public class WeatherData {

    /**
     * 온도 (섭씨)
     */
    private Double temperature;

    /**
     * 날씨 상태 (맑음, 흐림, 비, 눈 등)
     */
    private String condition;

    /**
     * 습도 (%)
     */
    private Double humidity;

    /**
     * 날씨 데이터 유효성 검증
     * 
     * @return 유효성 여부
     */
    public boolean isValid() {
        return temperature != null && 
               condition != null && !condition.trim().isEmpty() &&
               humidity != null && humidity >= 0 && humidity <= 100;
    }

    /**
     * 온도 기반 날씨 상태 설명
     * 
     * @return 날씨 상태 설명
     */
    public String getTemperatureDescription() {
        if (temperature == null) {
            return "알 수 없음";
        }
        
        if (temperature >= 30) {
            return "매우 더움";
        } else if (temperature >= 25) {
            return "더움";
        } else if (temperature >= 20) {
            return "따뜻함";
        } else if (temperature >= 10) {
            return "선선함";
        } else if (temperature >= 0) {
            return "춥다";
        } else {
            return "매우 춥다";
        }
    }
}
