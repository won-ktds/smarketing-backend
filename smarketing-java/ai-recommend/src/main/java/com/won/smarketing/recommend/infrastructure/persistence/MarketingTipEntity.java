package com.won.smarketing.recommend.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * 마케팅 팁 JPA 엔티티
 */
@Entity
@Table(name = "marketing_tips")
@EntityListeners(AuditingEntityListener.class)
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MarketingTipEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "store_id", nullable = false)
    private Long storeId;

    @Column(name = "tip_content", columnDefinition = "TEXT", nullable = false)
    private String tipContent;

    // WeatherData 임베디드
    @Column(name = "weather_temperature")
    private Double weatherTemperature;

    @Column(name = "weather_condition", length = 100)
    private String weatherCondition;

    @Column(name = "weather_humidity")
    private Double weatherHumidity;

    // StoreData 임베디드
    @Column(name = "store_name", length = 200)
    private String storeName;

    @Column(name = "business_type", length = 100)
    private String businessType;

    @Column(name = "store_location", length = 500)
    private String storeLocation;

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
}