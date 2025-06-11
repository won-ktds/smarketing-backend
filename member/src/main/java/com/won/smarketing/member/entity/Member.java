package com.won.smarketing.member.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstruct
재시도
Y
계속
편집
Member 서비스 모든 클래스 구현
코드 ∙ 버전 2 
   /**
     * 사용자 ID로 회원 조회
     * 
     * @param userId 사용자 ID
     * @return 회원 정보 (Optional)
     */
    Optional<Member> findByUserId(String userId);
    
    /**
     * 사용자 ID 존재 여부 확인
     * 
     * @param userId 사용자 ID
     * @return 존재 여부
 
Member 인증 서비스 구현체 및 Controllers
코드 