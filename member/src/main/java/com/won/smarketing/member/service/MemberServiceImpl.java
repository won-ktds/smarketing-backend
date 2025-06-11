package com.won.smarketing.member.service;

import com.won.smarketing.common.exception.BusinessException;
import com.won.smarketing.common.exception.ErrorCode;
import com.won.smarketing.member.dto.RegisterRequest;
import com.won.smarketing.member.dto.ValidationResponse;
import com.won.smarketing.member.entity.Member;
import com.won.smarketing.member.repository.MemberRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

/**
 * 회원 서비스 구현체
 * 회원 등록, 중복 확인, 패스워드 검증 기능 구현
 */
@Slf4j
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class MemberServiceImpl implements MemberService {

    private final MemberRepository memberRepository;
    private final PasswordEncoder passwordEncoder;
    
    // 패스워드 검증 패턴
    private static final Pattern LETTER_PATTERN = Pattern.compile(".*[a-zA-Z].*");
    private static final Pattern DIGIT_PATTERN = Pattern.compile(".*\\d.*");
    private static final Pattern SPECIAL_CHAR_PATTERN = Pattern.compile(".*[@$!%*?&].*");

    /**
     * 회원 등록
     * 
     * @param request 회원가입 요청 정보
     */
    @Override
    @Transactional
    public void register(RegisterRequest request) {
        log.info("회원 등록 시작: {}", request.getUserId());
        
        // 중복 확인
        if (memberRepository.existsByUserId(request.getUserId())) {
            throw new BusinessException(ErrorCode.DUPLICATE_MEMBER_ID);
        }
        
        if (memberRepository.existsByEmail(request.getEmail())) {
            throw new BusinessException(ErrorCode.DUPLICATE_EMAIL);
        }
        
        if (request.getBusinessNumber() != null && 
            memberRepository.existsByBusinessNumber(request.getBusinessNumber())) {
            throw new BusinessException(ErrorCode.DUPLICATE_BUSINESS_NUMBER);
        }
        
        // 회원 엔티티 생성 및 저장
        Member member = Member.builder()
                .userId(request.getUserId())
                .password(passwordEncoder.encode(request.getPassword()))
                .name(request.getName())
                .businessNumber(request.getBusinessNumber())
                .email(request.getEmail())
                .build();
        
        memberRepository.save(member);
        log.info("회원 등록 완료: {}", request.getUserId());
    }

    /**
     * 사용자 ID 중복 확인
     * 
     * @param userId 확인할 사용자 ID
     * @return 중복 여부
     */
    @Override
    public boolean checkDuplicate(String userId) {
        return memberRepository.existsByUserId(userId);
    }

    /**
     * 이메일 중복 확인
     * 
     * @param email 확인할 이메일
     * @return 중복 여부
     */
    @Override
    public boolean checkEmailDuplicate(String email) {
        return memberRepository.existsByEmail(email);
    }

    /**
     * 사업자번호 중복 확인
     * 
     * @param businessNumber 확인할 사업자번호
     * @return 중복 여부
     */
    @Override
    public boolean checkBusinessNumberDuplicate(String businessNumber) {
        if (businessNumber == null || businessNumber.trim().isEmpty()) {
            return false;
        }
        return memberRepository.existsByBusinessNumber(businessNumber);
    }

    /**
     * 패스워드 유효성 검증
     * 
     * @param password 검증할 패스워드
     * @return 검증 결과
     */
    @Override
    public ValidationResponse validatePassword(String password) {
        List<String> errors = new ArrayList<>();
        
        // 길이 검증
        if (password.length() < 8 || password.length() > 20) {
            errors.add("패스워드는 8-20자 사이여야 합니다");
        }
        
        // 영문 포함 여부
        if (!LETTER_PATTERN.matcher(password).matches()) {
            errors.add("영문이 포함되어야 합니다");
        }
        
        // 숫자 포함 여부
        if (!DIGIT_PATTERN.matcher(password).matches()) {
            errors.add("숫자가 포함되어야 합니다");
        }
        
        // 특수문자 포함 여부
        if (!SPECIAL_CHAR_PATTERN.matcher(password).matches()) {
            errors.add("특수문자(@$!%*?&)가 포함되어야 합니다");
        }
        
        if (errors.isEmpty()) {
            return ValidationResponse.valid("사용 가능한 패스워드입니다.");
        } else {
            return ValidationResponse.invalid("패스워드 규칙을 확인해 주세요.", errors);
        }
    }
}
