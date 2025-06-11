package com.won.smarketing.member.repository;

import com.won.smarketing.member.entity.Member;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * 회원 정보 데이터 접근을 위한 Repository
 * JPA를 사용한 회원 CRUD 작업 처리
 */
@Repository
public interface MemberRepository extends JpaRepository<Member, Long> {
    
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
     */
    boolean existsByUserId(String userId);
    
    /**
     * 이메일 존재 여부 확인
     * 
     * @param email 이메일
     * @return 존재 여부
     */
    boolean existsByEmail(String email);
    
    /**
     * 사업자번호 존재 여부 확인
     * 
     * @param businessNumber 사업자번호
     * @return 존재 여부
     */
    boolean existsByBusinessNumber(String businessNumber);
}
