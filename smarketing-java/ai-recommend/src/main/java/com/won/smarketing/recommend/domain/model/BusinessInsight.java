package com.won.smarketing.recommend.domain.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;

/**
 * 비즈니스 인사이트 엔티티
 */
@Entity
@Table(name = "business_insights")
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EntityListeners(AuditingEntityListener.class)
public class BusinessInsight {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "insight_id")
    private Long id;

    @Column(name = "store_id", nullable = false)
    private Long storeId;

    @Column(name = "insight_type", nullable = false, length = 50)
    private String insightType;

    @Column(name = "title", nullable = false, length = 200)
    private String title;

    @Column(name = "description", columnDefinition = "TEXT")
    private String description;

    @Column(name = "metric_value")
    private Double metricValue;

    @Column(name = "recommendation", columnDefinition = "TEXT")
    private String recommendation;

    @CreatedDate
    @Column(name = "created_at")
    private LocalDateTime createdAt;
}
