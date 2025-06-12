package com.won.smarketing.recommend.infrastructure.persistence;

import com.won.smarketing.recommend.domain.model.MarketingTip;
import com.won.smarketing.recommend.domain.model.StoreData;
import com.won.smarketing.recommend.domain.model.TipId;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * 마케팅 팁 JPA 엔티티 (날씨 정보 제거)
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

    @Column(name = "tip_content", nullable = false, length = 2000)
    private String tipContent;

    // 매장 정보만 저장
    @Column(name = "store_name", length = 200)
    private String storeName;

    @Column(name = "business_type", length = 100)
    private String businessType;

    @Column(name = "store_location", length = 500)
    private String storeLocation;

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    public static MarketingTipEntity fromDomain(MarketingTip marketingTip) {
        return MarketingTipEntity.builder()
                .id(marketingTip.getId() != null ? marketingTip.getId().getValue() : null)
                .storeId(marketingTip.getStoreId())
                .tipContent(marketingTip.getTipContent())
                .storeName(marketingTip.getStoreData().getStoreName())
                .businessType(marketingTip.getStoreData().getBusinessType())
                .storeLocation(marketingTip.getStoreData().getLocation())
                .createdAt(marketingTip.getCreatedAt())
                .build();
    }

    public MarketingTip toDomain() {
        StoreData storeData = StoreData.builder()
                .storeName(this.storeName)
                .businessType(this.businessType)
                .location(this.storeLocation)
                .build();

        return MarketingTip.builder()
                .id(this.id != null ? TipId.of(this.id) : null)
                .storeId(this.storeId)
                .tipContent(this.tipContent)
                .storeData(storeData)
                .createdAt(this.createdAt)
                .build();
    }
}
