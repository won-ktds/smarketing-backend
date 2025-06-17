package com.won.smarketing.content.infrastructure.entity;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;
import java.util.Date;

/**
 * 콘텐츠 JPA 엔티티
 */
@Entity
@Table(name = "contents")
@Getter
@Setter
@EntityListeners(AuditingEntityListener.class)
public class ContentJpaEntity {

    @Id
    @Column(name = "content_id")
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "store_id", nullable = false)
    private Long storeId;

    @Column(name = "content_type", nullable = false, length = 50)
    private String contentType;

    @Column(name = "platform", length = 50)
    private String platform;

    @Column(name = "title", length = 500)
    private String title;

    @Column(name = "PromotionStartDate")
    private LocalDateTime PromotionStartDate;

    @Column(name = "PromotionEndDate")
    private LocalDateTime PromotionEndDate;

    @Column(name = "content", columnDefinition = "TEXT")
    private String content;

    @Column(name = "hashtags", columnDefinition = "TEXT")
    private String hashtags;

    @Column(name = "images", columnDefinition = "TEXT")
    private String images;

    @Column(name = "status", nullable = false, length = 20)
    private String status;

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    // CreationConditions와의 관계 - OneToOne으로 별도 엔티티로 관리
    @OneToOne(mappedBy = "content", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private ContentConditionsJpaEntity conditions;
}