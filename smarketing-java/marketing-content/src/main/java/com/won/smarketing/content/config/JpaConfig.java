// marketing-content/src/main/java/com/won/smarketing/content/config/JpaConfig.java
package com.won.smarketing.content.config;

import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

/**
 * JPA 설정 클래스
 *
 * @author smarketing-team
 * @version 1.0
 */
@Configuration
@EntityScan(basePackages = "com.won.smarketing.content.infrastructure.entity")
@EnableJpaRepositories(basePackages = "com.won.smarketing.content.infrastructure.repository")
public class JpaConfig {
}