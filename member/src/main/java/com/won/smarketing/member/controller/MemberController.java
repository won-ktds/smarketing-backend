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
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;


/**
 * 회원 관리를 위한 REST API 컨트롤러
 * 회원가입, ID 중복 확인, 패스워드 유효성 검증 기능 제공
 */
@Tag(name = "회원 관리", description = "회원가입 및 회원 정보 관리 API")
@RestController
@RequestMapping("/api/member")
@RequiredArgsConstructor
public class MemberController {

    private final MemberService memberService;

    /**
     * 회원가입 처리
     * 
     * @param request 회원가입 요청 정보
     * @return 회원가입 성공/실패 응답
     */
    @Operation(summary = "회원가입", description = "새로운 회원을 등록합니다.")
    @PostMapping("/register")
    public ResponseEntity<ApiResponse<Void>> register(@Valid @RequestBody RegisterRequest request) {
        memberService.register(request);
        return ResponseEntity.ok(ApiResponse.success(null, "회원가입이 완료되었습니다."));
    }

    /**
     * ID 중복 확인
     * 
     * @param userId 확인할 사용자 ID
     * @return 중복 여부 응답
     */
    @Operation(summary = "ID 중복 확인", description = "사용자 ID의 중복 여부를 확인합니다.")
    @GetMapping("/check-duplicate")
    public ResponseEntity<ApiResponse<DuplicateCheckResponse>> checkDuplicate(
            @Parameter(description = "확인할 사용자 ID", required = true)
            @RequestParam String userId) {
        boolean isDuplicate = memberService.checkDuplicate(userId);
        DuplicateCheckResponse response = DuplicateCheckResponse.builder()
                .isDuplicate(isDuplicate)
                .message(isDuplicate ? "이미 사용 중인 ID입니다." : "사용 가능한 ID입니다.")
                .build();
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    /**
     * 패스워드 유효성 검증
     * 
     * @param request 패스워드 유효성 검증 요청
     * @return 유효성 검증 결과
     */
    @Operation(summary = "패스워드 유효성 검증", description = "패스워드가 보안 규칙을 만족하는지 확인합니다.")
    @PostMapping("/validate-password")
    public ResponseEntity<ApiResponse<ValidationResponse>> validatePassword(@Valid @RequestBody PasswordValidationRequest request) {
        ValidationResponse response = memberService.validatePassword(request.getPassword());
        return ResponseEntity.ok(ApiResponse.success(response));
    }
}
