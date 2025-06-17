package com.won.smarketing.content;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

/**
 * 마케팅 콘텐츠 서비스 메인 애플리케이션 클래스
 * Clean Architecture 패턴을 적용한 마케팅 콘텐츠 관리 서비스
 */
@SpringBootApplication(scanBasePackages = {
        "com.won.smarketing.content",
        "com.won.smarketing.common"
})
@EnableJpaRepositories(basePackages = {
        "com.won.smarketing.content.infrastructure.repository"
})
@EntityScan(basePackages = {
        "com.won.smarketing.content.infrastructure.entity"
})
@EnableJpaAuditing
public class MarketingContentServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(MarketingContentServiceApplication.class, args);
    }
}
