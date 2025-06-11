package com.won.smarketing.content.infrastructure.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDate;

/**
 * 콘텐츠 조건 JPA 엔티티
 *
 * @author smarketing-team
 * @version 1.0
 */
@Entity
@Table(name = "contents_conditions")
@Getter
@Setter
@NoArgsConstructor
public class ContentConditionsJpaEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne
    @JoinColumn(name = "content_id")
    private ContentJpaEntity content;

    @Column(name = "category", length = 100)
    private String category;

    @Column(name = "requirement", columnDefinition = "TEXT")
    private String requirement;

    @Column(name = "tone_and_manner", length = 100)
    private String toneAndManner;

    @Column(name = "emotion_intensity", length = 100)
    private String emotionIntensity;

    @Column(name = "event_name", length = 200)
    private String eventName;

    @Column(name = "start_date")
    private LocalDate startDate;

    @Column(name = "end_date")
    private LocalDate endDate;

    @Column(name = "photo_style", length = 100)
    private String photoStyle;

    @Column(name = "TargetAudience", length = 100)
    private String targetAudience;

    @Column(name = "PromotionType", length = 100)
    private String PromotionType;
}
