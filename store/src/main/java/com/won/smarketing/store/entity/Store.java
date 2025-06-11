package com.won.smarketing.store.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

/**
 * 매장 정보를 나타내는 엔티티
 * 매장의 기본 정보, 운영 정보, SNS 계정 정보 저장
 */
@Entity
@Table(name = "stores")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
@Builder
public class Store {

    /**
     * 매장 고유 식별자
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * 매장 소유자 사용자 ID
     */
    @Column(name = "user_id", unique = true, nullable = false, length = 50)
    private String userId;

    /**
     * 매장명
     */
    @Column(name = "store_name", nullable = false, length = 200)
    private String storeName;

    /**
     * 매장 이미지 URL
     */
    @Column(name = "store_image", length = 500)
    private String storeImage;

    /**
     * 업종
     */
    @Column(name = "business_type", nullable = false, length = 100)
    private String businessType;

    /**
     * 매장 주소
     */
    @Column(name = "address", nullable = false, length = 500)
    private String address;

    /**
     * 매장 전화번호
     */
    @Column(name = "phone_number", nullable = false, length = 20)
    private String phoneNumber;

    /**
     * 사업자 번호
     */
    @Column(name = "business_number", nullable = false, length = 20)
    private String businessNumber;

    /**
     * 인스타그램 계정
     */
    @Column(name = "insta_account", length = 100)
    private String instaAccount;

    /**
     * 네이버 블로그 계정
     */
    @Column(name = "naver_blog_account", length = 100)
    private String naverBlogAccount;

    /**
     * 오픈 시간
     */
    @Column(name = "open_time", length = 10)
    private String openTime;

    /**
     * 마감 시간
     */
    @Column(name = "close_time", length = 10)
    private String closeTime;

    /**
     * 휴무일
     */
    @Column(name = "closed_days", length = 100)
    private String closedDays;

    /**
     * 좌석 수
     */
    @Column(name = "seat_count")
    private Integer seatCount;

    /**
     * 매장 등록 시각
     */
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    /**
     * 매장 정보 수정 시각
     */
    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;

    /**
     * 엔티티 저장 전 실행되는 메서드
     * 생성 시각과 수정 시각을 현재 시각으로 설정
     */
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    /**
     * 엔티티 업데이트 전 실행되는 메서드
     * 수정 시각을 현재 시각으로 갱신
     */
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }

    /**
     * 매장 정보 업데이트 메서드
     * 
     * @param storeName 매장명
     * @param storeImage 매장 이미지
     * @param address 주소
     * @param phoneNumber 전화번호
     * @param instaAccount 인스타그램 계정
     * @param naverBlogAccount 네이버 블로그 계정
     * @param openTime 오픈 시간
     * @param closeTime 마감 시간
     * @param closedDays 휴무일
     * @param seatCount 좌석 수
     */
    public void updateStoreInfo(String storeName, String storeImage, String address, String phoneNumber,
                               String instaAccount, String naverBlogAccount, String openTime, String closeTime,
                               String closedDays, Integer seatCount) {
        this.storeName = storeName;
        this.storeImage = storeImage;
        this.address = address;
        this.phoneNumber = phoneNumber;
        this.instaAccount = instaAccount;
        this.naverBlogAccount = naverBlogAccount;
        this.openTime = openTime;
        this.closeTime = closeTime;
        this.closedDays = closedDays;
        this.seatCount = seatCount;
    }
}
