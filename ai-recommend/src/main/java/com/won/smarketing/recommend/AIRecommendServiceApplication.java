package com.won.smarketing.recommend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

/**
 * AI 추천 서비스 메인 애플리케이션 클래스
 * Clean Architecture 패턴을 적용한 AI 마케팅 추천 서비스
 */
@SpringBootApplication(scanBasePackages = {"com.won.smarketing.recommend", "com.won.smarketing.common"})
@EntityScan(basePackages = {"com.won.smarketing.recommend.infrastructure.entity"})
@EnableJpaRepositories(basePackages = {"com.won.smarketing.recommend.infrastructure.repository"})
public class AIRecommendServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(AIRecommendServiceApplication.class, args);
    }
}
