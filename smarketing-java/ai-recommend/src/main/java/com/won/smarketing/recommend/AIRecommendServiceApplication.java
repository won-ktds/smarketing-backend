package com.won.smarketing.recommend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

/**
 * AI 추천 서비스 메인 애플리케이션
 */
@SpringBootApplication
@EnableJpaAuditing
@EnableCaching
public class AIRecommendServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(AIRecommendServiceApplication.class, args);
    }
}
