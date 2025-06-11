package com.won.smarketing.member.service;

import com.won.smarketing.member.dto.RegisterRequest;
import com.won.smarketing.member.dto.ValidationResponse;

/**
 * 회원 관리 서비스 인터페이스
 * 회원가입, 중복 확인, 패스워드 유효성 검증 기능 정의
 */
public interface MemberService {
    
    /**
     * 회원가입 처리
     * 
     * @param request 회원가입 요청 정보
     */
    void register(RegisterRequest request);
    
    /**
     * 사용자 ID 중복 확인
     * 
     * @param userId 확인할 사용자 ID
     * @return 중복 여부 (true: 중복, false: 사용 가능)
     */
    boolean checkDuplicate(String userId);
    
    /**
     * 패스워드 유효성 검증
     * 
     * @param password 검증할 패스워드
     * @return 유효성 검증 결과
     */
    ValidationResponse validatePassword(String password);
}
