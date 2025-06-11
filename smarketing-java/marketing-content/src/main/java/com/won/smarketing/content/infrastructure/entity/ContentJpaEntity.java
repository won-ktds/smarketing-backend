// marketing-content/src/main/java/com/won/smarketing/content/infrastructure/entity/ContentJpaEntity.java
package com.won.smarketing.content.infrastructure.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 콘텐츠 JPA 엔티티
 *
 * @author smarketing-team
 * @version 1.0
 */
@Entity
@Table(name = "contents")
@Getter
@Setter
@NoArgsConstructor
public class ContentJpaEntity {

    @Id
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

    @Column(name = "content", columnDefinition = "TEXT")
    private String content;

    @Column(name = "hashtags", columnDefinition = "JSON")
    private String hashtags;

    @Column(name = "images", columnDefinition = "JSON")
    private String images;

    @Column(name = "status", length = 50)
    private String status;

    @CreationTimestamp
    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    // 연관 엔티티
    @OneToOne(mappedBy = "content", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private ContentConditionsJpaEntity conditions;
}