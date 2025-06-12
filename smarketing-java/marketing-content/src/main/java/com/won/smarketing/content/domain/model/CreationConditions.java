// marketing-content/src/main/java/com/won/smarketing/content/domain/model/CreationConditions.java
package com.won.smarketing.content.domain.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

/**
 * 콘텐츠 생성 조건 도메인 모델
 * Clean Architecture의 Domain Layer에 위치하는 값 객체
 */
@Entity
@Table(name = "contents_conditions")
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CreationConditions {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    //@OneToOne(mappedBy = "creationConditions")
    @Column(name = "content", length = 100)
    private Content content;

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

    @Column(name = "promotionType", length = 100)
    private String promotionType;

    public CreationConditions(String category, String requirement, String toneAndManner, String emotionIntensity, String eventName, LocalDate startDate, LocalDate endDate, String photoStyle, String promotionType) {
    }
//    /**
//     * 콘텐츠와의 연관관계 설정
//     * @param content 연관된 콘텐츠
//     */
//    public void setContent(Content content) {
//        this.content = content;
//    }
}