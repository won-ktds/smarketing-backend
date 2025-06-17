package com.won.smarketing.recommend.infrastructure.persistence;

import com.won.smarketing.recommend.domain.model.MarketingTip;
import com.won.smarketing.recommend.domain.model.StoreData;
import com.won.smarketing.recommend.domain.model.TipId;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
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
    @Column(name = "tip_id", nullable = false)
    private Long id;

    @Column(name = "user_id", nullable = false, length = 50)
    private String userId;

    @Column(name = "store_id", nullable = false)
    private Long storeId;

    @Column(name = "tip_summary")
    private String tipSummary;

    @Lob
    @Column(name = "tip_content", nullable = false, columnDefinition = "TEXT")
    private String tipContent;

    @Column(name = "ai_model")
    private String aiModel;

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    public static MarketingTipEntity fromDomain(MarketingTip marketingTip, String userId) {
        return MarketingTipEntity.builder()
                .id(marketingTip.getId() != null ? marketingTip.getId().getValue() : null)
                .userId(userId)
                .storeId(marketingTip.getStoreId())
                .tipContent(marketingTip.getTipContent())
                .tipSummary(marketingTip.getTipSummary())
                .createdAt(marketingTip.getCreatedAt())
                .updatedAt(marketingTip.getUpdatedAt())
                .build();
    }


    public MarketingTip toDomain(StoreData storeData) {
        return MarketingTip.builder()
                .id(this.id != null ? TipId.of(this.id) : null)
                .storeId(this.storeId)
                .tipSummary(this.tipSummary)
                .tipContent(this.tipContent)
                .createdAt(this.createdAt)
                .updatedAt(this.updatedAt)
                .build();
    }
}
