package com.won.smarketing.content.domain.model;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

/**
 * 콘텐츠 타입 열거형
 * 지원되는 마케팅 콘텐츠 유형 정의
 */
@Getter
@RequiredArgsConstructor
public enum ContentType {
    
    SNS_POST("SNS 게시물"),
    POSTER("홍보 포스터");

    private final String displayName;

    /**
     * 문자열로부터 ContentType 변환
     * 
     * @param type 타입 문자열
     * @return ContentType
     */
    public static ContentType fromString(String type) {
        if (type == null) {
            return null;
        }
        
        for (ContentType contentType : ContentType.values()) {
            if (contentType.name().equalsIgnoreCase(type)) {
                return contentType;
            }
        }
        
        throw new IllegalArgumentException("알 수 없는 콘텐츠 타입: " + type);
    }
}
