package com.won.smarketing.content.domain.model;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

/**
 * 플랫폼 열거형
 * 콘텐츠가 게시될 플랫폼 정의
 */
@Getter
@RequiredArgsConstructor
public enum Platform {
    
    INSTAGRAM("인스타그램"),
    NAVER_BLOG("네이버 블로그"),
    GENERAL("범용");

    private final String displayName;

    /**
     * 문자열로부터 Platform 변환
     * 
     * @param platform 플랫폼 문자열
     * @return Platform
     */
    public static Platform fromString(String platform) {
        if (platform == null) {
            return GENERAL;
        }
        
        for (Platform p : Platform.values()) {
            if (p.name().equalsIgnoreCase(platform)) {
                return p;
            }
        }
        
        throw new IllegalArgumentException("알 수 없는 플랫폼: " + platform);
    }
}
