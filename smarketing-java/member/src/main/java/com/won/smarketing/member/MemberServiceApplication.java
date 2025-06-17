package com.won.smarketing.member;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

/**
 * 회원 서비스 메인 애플리케이션 클래스
 * Spring Boot 애플리케이션의 진입점
 */
@SpringBootApplication(scanBasePackages = {"com.won.smarketing.member", "com.won.smarketing.common"})
@EntityScan(basePackages = {"com.won.smarketing.member.entity"})
@EnableJpaRepositories(basePackages = {"com.won.smarketing.member.repository"})
public class MemberServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(MemberServiceApplication.class, args);
    }
}
