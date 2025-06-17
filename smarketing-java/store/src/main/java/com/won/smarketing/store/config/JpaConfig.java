package com.won.smarketing.store.config;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

/**
 * JPA 설정 클래스
 * JPA Auditing 기능 활성화
 */
@Configuration
@EnableJpaAuditing
public class JpaConfig {
    private String category;
    
    @Schema(description = "가격", example = "4500", required = true)
    @NotNull(message = "가격은 필수입니다")
    @Min(value = 0, message = "가격은 0원 이상이어야 합니다")
    private Integer price;
    
    @Schema(description = "메뉴 설명", example = "진한 맛의 아메리카노")
    @Size(max = 500, message = "메뉴 설명은 500자 이하여야 합니다")
    private String description;
    
    @Schema(description = "이미지 URL", example = "https://example.com/americano.jpg")
    @Size(max = 500, message = "이미지 URL은 500자 이하여야 합니다")
    private String image;
}
