package com.won.smarketing.store.entity;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * 매출 정보를 나타내는 엔티티
 * 일별 매출 데이터 저장
 */
@Entity
@Table(name = "sales")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
@Builder
public class Sales {

    /**
     * 매출 고유 식별자
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * 매장 ID
     */
    @Column(name = "store_id", nullable = false)
    private Long storeId;

    /**
     * 매출 날짜
     */
    @Column(name = "sales_date", nullable = false)
    private LocalDate salesDate;

    /**
     * 매출 금액
     */
    @Column(name = "sales_amount", nullable = false, precision = 15, scale = 2)
    private BigDecimal salesAmount;

    /**
     * 매출 등록 시각
     */
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    /**
     * 엔티티 저장 전 실행되는 메서드
     * 생성 시각을 현재 시각으로 설정
     */
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
}
