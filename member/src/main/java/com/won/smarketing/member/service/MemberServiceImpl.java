package com.won.smarketing.member.service;

import com.won.smarketing.common.exception.BusinessException;
import com.won.smarketing.common.exception.ErrorCode;
import com.won.smarketing.member.dto.RegisterRequest;
import com.won.smarketing.member.dto.ValidationResponse;
import com.won.smarketing.member.entity.Member;
import com.won.smarketing.member.repository.MemberRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

/**
 * 회원 관리 서비스 구현체
 * 회원가입, 중복 확인, 패스워드 유효성 검증 기능 구현
 */
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class MemberServiceImpl implements MemberService {

    private final MemberRepository memberRepository;
    private final PasswordEncoder passwordEncoder;

    // 패스워드 정규식: 영문, 숫자, 특수문자 각각 최소 1개 포함, 8자 이상
    private static final Pattern PASSWORD_PATTERN = Pattern.compile(
            "^(?=.*[a-zA-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$"
    );

    /**
     * 회원가입 처리
     * 
     * @param request 회원가입 요청 정보
     */
    @Override
    @Transactional
    public void register(RegisterRequest request) {
        // 중복 ID 확인
        if (memberRepository.existsByUserId(request.getUserId())) {
            throw new BusinessException(ErrorCode.DUPLICATE_MEMBER_ID);
        }

        // 이메일 중복 확인
        if (memberRepository.existsByEmail(request.getEmail())) {
            throw new BusinessException(ErrorCode.DUPLICATE_EMAIL);
        }

        // 사업자 번호 중복 확인
        if (memberRepository.existsByBusinessNumber(request.getBusinessNumber())) {
            throw new BusinessException(ErrorCode.DUPLICATE_BUSINESS_NUMBER);
        }

        // 패스워드 암호화
        String encodedPassword = passwordEncoder.encode(request.getPassword());

        // 회원 엔티티 생성 및 저장
        Member member = Member.builder()
                .userId(request.getUserId())
                .password(encodedPassword)
                .name(request.getName())
                .businessNumber(request.getBusinessNumber())
                .email(request.getEmail())
                .build();

        memberRepository.save(member);
    }

    /**
     * 사용자 ID 중복 확인
     * 
     * @param userId 확인할 사용자 ID
     * @return 중복 여부 (true: 중복, false: 사용 가능)
     */
    @Override
    public boolean checkDuplicate(String userId) {
        return memberRepository.existsByUserId(userId);
    }

    /**
     * 패스워드 유효성 검증
     * 
     * @param password 검증할 패스워드
     * @return 유효성 검증 결과
     */
    @Override
    public ValidationResponse validatePassword(String password) {
        List<String> errors = new ArrayList<>();
        boolean isValid = true;

        // 길이 검증 (8자 이상)
        if (password.length() < 8) {
            errors.add("패스워드는 8자 이상이어야 합니다.");
            isValid = false;
        }

        // 패턴 검증 (영문, 숫자, 특수문자 포함)
        if (!PASSWORD_PATTERN.matcher(password).matches()) {
            errors.add("패스워드는 영문, 숫자, 특수문자를 각각 최소 1개씩 포함해야 합니다.");
            isValid = false;
        }

        String message = isValid ? "유효한 패스워드입니다." : "패스워드가 보안 규칙을 만족하지 않습니다.";

        return ValidationResponse.builder()
                .isValid(isValid)
                .message(message)
                .errors(errors)
                .build();
    }
}
