package com.won.smarketing.store.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

/**
 * 메뉴 정보를 나타내는 엔티티
 * 메뉴명, 카테고리, 가격, 설명, 이미지 정보 저장
 */
@Entity
@Table(name = "menus")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
@Builder
public class Menu {

    /**
     * 메뉴 고유 식별자
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
     * 메뉴명
     */
    @Column(name = "menu_name", nullable = false, length = 200)
    private String menuName;

    /**
     * 메뉴 카테고리
     */
    @Column(name = "category", nullable = false, length = 100)
    private String category;

    /**
     * 가격
     */
    @Column(name = "price", nullable = false)
    private Integer price;

    /**
     * 메뉴 설명
     */
    @Column(name = "description", columnDefinition = "TEXT")
    private String description;

    /**
     * 메뉴 이미지 URL
     */
    @Column(name = "image", length = 500)
    private String image;

    /**
     * 메뉴 등록 시각
     */
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    /**
     * 메뉴 정보 수정 시각
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
     * 메뉴 정보 업데이트 메서드
     * 
     * @param menuName 메뉴명
     * @param category 카테고리
     * @param price 가격
     * @param description 설명
     * @param image 이미지 URL
     */
    public void updateMenuInfo(String menuName, String category, Integer price, String description, String image) {
        this.menuName = menuName;
        this.category = category;
        this.price = price;
        this.description = description;
        this.image = image;
    }
}
