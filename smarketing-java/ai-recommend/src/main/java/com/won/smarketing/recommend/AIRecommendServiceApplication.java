package com.won.smarketing.recommend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication(scanBasePackages = {
    "com.won.smarketing.recommend",
    "com.won.smarketing.common"
})
@EnableJpaAuditing
@EnableJpaRepositories(basePackages = "com.won.smarketing.recommend.infrastructure.persistence")
@EnableCaching
public class AIRecommendServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(AIRecommendServiceApplication.class, args);
    }
}
