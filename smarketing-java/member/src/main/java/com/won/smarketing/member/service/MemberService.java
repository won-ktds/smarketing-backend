package com.won.smarketing.member.service;

import com.won.smarketing.member.dto.RegisterRequest;
import com.won.smarketing.member.dto.ValidationResponse;

/**
 * 회원 서비스 인터페이스
 * 회원 관리 관련 비즈니스 로직 정의
 */
public interface MemberService {
    
    /**
     * 회원 등록
     * 
     * @param request 회원가입 요청 정보
     */
    void register(RegisterRequest request);
    
    /**
     * 사용자 ID 중복 확인
     * 
     * @param userId 확인할 사용자 ID
     * @return 중복 여부
     */
    boolean checkDuplicate(String userId);
    
    /**
     * 이메일 중복 확인
     * 
     * @param email 확인할 이메일
     * @return 중복 여부
     */
    boolean checkEmailDuplicate(String email);
    
    /**
     * 사업자번호 중복 확인
     * 
     * @param businessNumber 확인할 사업자번호
     * @return 중복 여부
     */
    boolean checkBusinessNumberDuplicate(String businessNumber);
    
    /**
     * 패스워드 유효성 검증
     * 
     * @param password 검증할 패스워드
     * @return 검증 결과
     */
    ValidationResponse validatePassword(String password);
}
