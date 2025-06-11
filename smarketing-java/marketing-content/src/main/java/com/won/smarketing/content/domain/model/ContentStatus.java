package com.won.smarketing.content.domain.model;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

/**
 * 콘텐츠 상태 열거형
 * 콘텐츠의 생명주기 상태 정의
 */
@Getter
@RequiredArgsConstructor
public enum ContentStatus {
    
    DRAFT("임시저장"),
    PUBLISHED("발행됨"),
    ARCHIVED("보관됨");

    private final String displayName;

    /**
     * 문자열로부터 ContentStatus 변환
     * 
     * @param status 상태 문자열
     * @return ContentStatus
     */
    public static ContentStatus fromString(String status) {
        if (status == null) {
            return DRAFT;
        }
        
        for (ContentStatus s : ContentStatus.values()) {
            if (s.name().equalsIgnoreCase(status)) {
                return s;
            }
        }
        
        throw new IllegalArgumentException("알 수 없는 콘텐츠 상태: " + status);
    }
}
