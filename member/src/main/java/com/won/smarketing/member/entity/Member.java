package com.won.smarketing.member.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

/**
 * 회원 정보를 나타내는 엔티티
 * 사용자 ID, 패스워드, 이름, 사업자 번호, 이메일 정보 저장
 */
@Entity
@Table(name = "members")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
@Builder
public class Member {

    /**
     * 회원 고유 식별자
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * 사용자 ID (로그인용)
     */
    @Column(name = "user_id", unique = true, nullable = false, length = 50)
    private String userId;

    /**
     * 암호화된 패스워드
     */
    @Column(name = "password", nullable = false)
    private String password;

    /**
     * 회원 이름
     */
    @Column(name = "name", nullable = false, length = 100)
    private String name;

    /**
     * 사업자 번호
     */
    @Column(name = "business_number", unique = true, nullable = false, length = 20)
    private String businessNumber;

    /**
     * 이메일 주소
     */
    @Column(name = "email", unique = true, nullable = false)
    private String email;

    /**
     * 회원 생성 시각
     */
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    /**
     * 회원 정보 수정 시각
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
}
