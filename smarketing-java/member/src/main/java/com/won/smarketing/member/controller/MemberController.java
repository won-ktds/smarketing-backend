package com.won.smarketing.member.controller;

import com.won.smarketing.common.dto.ApiResponse;
import com.won.smarketing.member.dto.DuplicateCheckResponse;
import com.won.smarketing.member.dto.PasswordValidationRequest;
import com.won.smarketing.member.dto.RegisterRequest;
import com.won.smarketing.member.dto.ValidationResponse;
import com.won.smarketing.member.service.MemberService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;

/**
 * 회원 관리를 위한 REST API 컨트롤러
 * 회원가입, 중복 확인, 패스워드 검증 기능 제공
 */
@Tag(name = "회원 관리", description = "회원가입 및 회원 정보 관리 API")
@RestController
@RequestMapping("/api/member")
@RequiredArgsConstructor
public class MemberController {

    private final MemberService memberService;

    /**
     * 회원가입
     * 
     * @param request 회원가입 요청 정보
     * @return 회원가입 성공 응답
     */
    @Operation(summary = "회원가입", description = "새로운 회원을 등록합니다.")
    @PostMapping("/register")
    public ResponseEntity<ApiResponse<Void>> register(@Valid @RequestBody RegisterRequest request) {
        memberService.register(request);
        return ResponseEntity.ok(ApiResponse.success(null, "회원가입이 완료되었습니다."));
    }

    /**
     * 사용자 ID 중복 확인
     * 
     * @param userId 확인할 사용자 ID
     * @return 중복 확인 결과
     */
    @Operation(summary = "사용자 ID 중복 확인", description = "사용자 ID의 중복 여부를 확인합니다.")
    @GetMapping("/check-duplicate/user-id")
    public ResponseEntity<ApiResponse<DuplicateCheckResponse>> checkUserIdDuplicate(
            @Parameter(description = "확인할 사용자 ID", required = true)
            @RequestParam String userId) {
        
        boolean isDuplicate = memberService.checkDuplicate(userId);
        DuplicateCheckResponse response = isDuplicate 
                ? DuplicateCheckResponse.duplicate("이미 사용 중인 사용자 ID입니다.")
                : DuplicateCheckResponse.available("사용 가능한 사용자 ID입니다.");
        
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    /**
     * 이메일 중복 확인
     * 
     * @param email 확인할 이메일
     * @return 중복 확인 결과
     */
    @Operation(summary = "이메일 중복 확인", description = "이메일의 중복 여부를 확인합니다.")
    @GetMapping("/check-duplicate/email")
    public ResponseEntity<ApiResponse<DuplicateCheckResponse>> checkEmailDuplicate(
            @Parameter(description = "확인할 이메일", required = true)
            @RequestParam String email) {
        
        boolean isDuplicate = memberService.checkEmailDuplicate(email);
        DuplicateCheckResponse response = isDuplicate 
                ? DuplicateCheckResponse.duplicate("이미 사용 중인 이메일입니다.")
                : DuplicateCheckResponse.available("사용 가능한 이메일입니다.");
        
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    /**
     * 사업자번호 중복 확인
     * 
     * @param businessNumber 확인할 사업자번호
     * @return 중복 확인 결과
     */
    @Operation(summary = "사업자번호 중복 확인", description = "사업자번호의 중복 여부를 확인합니다.")
    @GetMapping("/check-duplicate/business-number")
    public ResponseEntity<ApiResponse<DuplicateCheckResponse>> checkBusinessNumberDuplicate(
            @Parameter(description = "확인할 사업자번호", required = true)
            @RequestParam String businessNumber) {
        
        boolean isDuplicate = memberService.checkBusinessNumberDuplicate(businessNumber);
        DuplicateCheckResponse response = isDuplicate 
                ? DuplicateCheckResponse.duplicate("이미 등록된 사업자번호입니다.")
                : DuplicateCheckResponse.available("사용 가능한 사업자번호입니다.");
        
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    /**
     * 패스워드 유효성 검증
     * 
     * @param request 패스워드 검증 요청
     * @return 패스워드 검증 결과
     */
    @Operation(summary = "패스워드 검증", description = "패스워드가 규칙을 만족하는지 확인합니다.")
    @PostMapping("/validate-password")
    public ResponseEntity<ApiResponse<ValidationResponse>> validatePassword(
            @Valid @RequestBody PasswordValidationRequest request) {
        
        ValidationResponse response = memberService.validatePassword(request.getPassword());
        return ResponseEntity.ok(ApiResponse.success(response));
    }
}



