package com.won.smarketing.recommend.config;

import org.springframework.cache.annotation.EnableCaching;
import org.springframework.context.annotation.Configuration;

/**
 * 캐시 설정
 */
@Configuration
@EnableCaching
public class CacheConfig {
    // 기본 Simple 캐시 사용
}
