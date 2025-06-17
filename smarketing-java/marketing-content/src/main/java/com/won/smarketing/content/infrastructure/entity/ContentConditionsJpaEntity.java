// marketing-content/src/main/java/com/won/smarketing/content/infrastructure/entity/ContentConditionsJpaEntity.java
package com.won.smarketing.content.infrastructure.entity;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDate;

/**
 * 콘텐츠 생성 조건 JPA 엔티티
 * Infrastructure Layer에서 데이터베이스 매핑을 담당
 */
@Entity
@Table(name = "content_conditions")
@Getter
@Setter
public class ContentConditionsJpaEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "content_id", nullable = false)
    private ContentJpaEntity content;

    @Column(name = "category", length = 100)
    private String category;

    @Column(name = "requirement", columnDefinition = "TEXT")
    private String requirement;

    @Column(name = "tone_and_manner", length = 100)
    private String toneAndManner;

    @Column(name = "emotion_intensity", length = 50)
    private String emotionIntensity;

    @Column(name = "event_name", length = 200)
    private String eventName;

    @Column(name = "start_date")
    private LocalDate startDate;

    @Column(name = "end_date")
    private LocalDate endDate;

    @Column(name = "photo_style", length = 100)
    private String photoStyle;

    @Column(name = "promotion_type", length = 100)
    private String promotionType;

    // 생성자
    public ContentConditionsJpaEntity(ContentJpaEntity content, String category, String requirement,
                                      String toneAndManner, String emotionIntensity, String eventName,
                                      LocalDate startDate, LocalDate endDate, String photoStyle, String promotionType) {
        this.content = content;
        this.category = category;
        this.requirement = requirement;
        this.toneAndManner = toneAndManner;
        this.emotionIntensity = emotionIntensity;
        this.eventName = eventName;
        this.startDate = startDate;
        this.endDate = endDate;
        this.photoStyle = photoStyle;
        this.promotionType = promotionType;
    }

    public ContentConditionsJpaEntity() {

    }

    // 팩토리 메서드
    public static ContentConditionsJpaEntity create(ContentJpaEntity content, String category, String requirement,
                                                    String toneAndManner, String emotionIntensity, String eventName,
                                                    LocalDate startDate, LocalDate endDate, String photoStyle, String promotionType) {
        return new ContentConditionsJpaEntity(content, category, requirement, toneAndManner, emotionIntensity,
                eventName, startDate, endDate, photoStyle, promotionType);
    }
}