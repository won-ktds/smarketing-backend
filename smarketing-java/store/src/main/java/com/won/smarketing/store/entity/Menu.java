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

/**
 * 메뉴 엔티티
 * 매장의 메뉴 정보를 관리
 */
@Entity
@Table(name = "menus")
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EntityListeners(AuditingEntityListener.class)
public class Menu {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "menu_id")
    private Long menuId;

    @Column(name = "store_id", nullable = false)
    private Long storeId;

    @Column(name = "menu_name", nullable = false, length = 100)
    private String menuName;

    @Column(name = "category", length = 50)
    private String category;

    @Column(name = "price", nullable = false)
    private Integer price;

    @Column(name = "description", length = 500)
    private String description;

    @Column(name = "image_url", length = 500)
    private String image;

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    /**
     * 메뉴 정보 업데이트
     * 
     * @param menuName 메뉴명
     * @param category 카테고리
     * @param price 가격
     * @param description 설명
     */
    public void updateMenu(String menuName, String category, Integer price, 
                          String description) {
        if (menuName != null && !menuName.trim().isEmpty()) {
            this.menuName = menuName;
        }
        if (category != null && !category.trim().isEmpty()) {
            this.category = category;
        }
        if (price != null && price > 0) {
            this.price = price;
        }
        this.description = description;
    }

    /**
     * 메뉴 이미지 URL 업데이트
     *
     * @param imageUrl 새로운 이미지 URL
     */
    public void updateImage(String imageUrl) {
        this.image = imageUrl;
        this.updatedAt = LocalDateTime.now();
    }

}
