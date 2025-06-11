package com.won.smarketing.store.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;
import java.time.LocalTime;

/**
 * 매장 엔티티
 * 매장의 기본 정보와 운영 정보를 관리
 */
@Entity
@Table(name = "stores")
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EntityListeners(AuditingEntityListener.class)
public class Store {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "store_id")
    private Long id;

    @Column(name = "member_id", nullable = false)
    private Long memberId;

    @Column(name = "store_name", nullable = false, length = 100)
    private String storeName;

    @Column(name = "business_type", length = 50)
    private String businessType;

    @Column(name = "address", nullable = false, length = 200)
    private String address;

    @Column(name = "phone_number", length = 20)
    private String phoneNumber;

    @Column(name = "business_hours", length = 100)
    private String businessHours;

    @Column(name = "closed_days", length = 100)
    private String closedDays;

    @Column(name = "seat_count")
    private Integer seatCount;

    @Column(name = "sns_accounts", length = 500)
    private String snsAccounts;

    @Column(name = "description", length = 1000)
    private String description;

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    /**
     * 매장 정보 업데이트
     * 
     * @param storeName 매장명
     * @param businessType 업종
     * @param address 주소
     * @param phoneNumber 전화번호
     * @param businessHours 영업시간
     * @param closedDays 휴무일
     * @param seatCount 좌석 수
     * @param snsAccounts SNS 계정 정보
     * @param description 설명
     */
    public void updateStore(String storeName, String businessType, String address,
                           String phoneNumber, String businessHours, String closedDays,
                           Integer seatCount, String snsAccounts, String description) {
        if (storeName != null && !storeName.trim().isEmpty()) {
            this.storeName = storeName;
        }
        if (businessType != null && !businessType.trim().isEmpty()) {
            this.businessType = businessType;
        }
        if (address != null && !address.trim().isEmpty()) {
            this.address = address;
        }
        this.phoneNumber = phoneNumber;
        this.businessHours = businessHours;
        this.closedDays = closedDays;
        this.seatCount = seatCount;
        this.snsAccounts = snsAccounts;
        this.description = description;
    }
}
