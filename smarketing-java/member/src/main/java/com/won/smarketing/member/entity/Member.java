package com.won.smarketing.member.entity;

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
 * 회원 엔티티
 * 회원의 기본 정보와 사업자 정보를 관리
 */
@Entity
@Table(name = "members")
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EntityListeners(AuditingEntityListener.class)
public class Member {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long id;

    @Column(name = "user_id", nullable = false, unique = true, length = 50)
    private String userId;

    @Column(name = "password", nullable = false, length = 100)
    private String password;

    @Column(name = "name", nullable = false, length = 50)
    private String name;

    @Column(name = "business_number", length = 12)
    private String businessNumber;

    @Column(name = "email", nullable = false, unique = true, length = 100)
    private String email;

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    /**
     * 회원 정보 업데이트
     *
     * @param name 이름
     * @param email 이메일
     * @param businessNumber 사업자번호
     */
    public void updateProfile(String name, String email, String businessNumber) {
        if (name != null && !name.trim().isEmpty()) {
            this.name = name;
        }
        if (email != null && !email.trim().isEmpty()) {
            this.email = email;
        }
        if (businessNumber != null && !businessNumber.trim().isEmpty()) {
            this.businessNumber = businessNumber;
        }
    }

    /**
     * 패스워드 변경
     *
     * @param encodedPassword 암호화된 패스워드
     */
    public void changePassword(String encodedPassword) {
        this.password = encodedPassword;
    }
}
