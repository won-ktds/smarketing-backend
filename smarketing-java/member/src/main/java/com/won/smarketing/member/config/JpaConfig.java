package com.won.smarketing.member.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

/**
 * JPA 설정 클래스
 * JPA Auditing 기능 활성화
 */
@Configuration
@EnableJpaAuditing
public class JpaConfig {
}
