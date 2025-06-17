package com.won.smarketing.content.presentation.controller;

import com.won.smarketing.common.dto.ApiResponse;
import com.won.smarketing.content.application.usecase.ContentQueryUseCase;
import com.won.smarketing.content.application.usecase.PosterContentUseCase;
import com.won.smarketing.content.application.usecase.SnsContentUseCase;
import com.won.smarketing.content.presentation.dto.*;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;
import java.util.List;

/**
 * 마케팅 콘텐츠 관리를 위한 REST API 컨트롤러
 * SNS 콘텐츠 생성, 포스터 생성, 콘텐츠 관리 기능 제공
 */
@Tag(name = "마케팅 콘텐츠 관리", description = "AI 기반 마케팅 콘텐츠 생성 및 관리 API")
@RestController
@RequestMapping("/api/content")
@RequiredArgsConstructor
public class ContentController {

    private final SnsContentUseCase snsContentUseCase;
    private final PosterContentUseCase posterContentUseCase;
    private final ContentQueryUseCase contentQueryUseCase;

    /**
     * SNS 게시물 생성
     * 
     * @param request SNS 콘텐츠 생성 요청
     * @return 생성된 SNS 콘텐츠 정보
     */
    @Operation(summary = "SNS 게시물 생성", description = "AI를 활용하여 SNS 게시물을 생성합니다.")
    @PostMapping("/sns/generate")
    public ResponseEntity<ApiResponse<SnsContentCreateResponse>> generateSnsContent(@Valid @RequestBody SnsContentCreateRequest request) {
        SnsContentCreateResponse response = snsContentUseCase.generateSnsContent(request);
        return ResponseEntity.ok(ApiResponse.success(response, "SNS 콘텐츠가 성공적으로 생성되었습니다."));
    }

    /**
     * SNS 게시물 저장
     * 
     * @param request SNS 콘텐츠 저장 요청
     * @return 저장 성공 응답
     */
    @Operation(summary = "SNS 게시물 저장", description = "생성된 SNS 게시물을 저장합니다.")
    @PostMapping("/sns/save")
    public ResponseEntity<ApiResponse<Void>> saveSnsContent(@Valid @RequestBody SnsContentSaveRequest request) {
        snsContentUseCase.saveSnsContent(request);
        return ResponseEntity.ok(ApiResponse.success(null, "SNS 콘텐츠가 성공적으로 저장되었습니다."));
    }

    /**
     * 홍보 포스터 생성
     * 
     * @param request 포스터 콘텐츠 생성 요청
     * @return 생성된 포스터 콘텐츠 정보
     */
    @Operation(summary = "홍보 포스터 생성", description = "AI를 활용하여 홍보 포스터를 생성합니다.")
    @PostMapping("/poster/generate")
    public ResponseEntity<ApiResponse<PosterContentCreateResponse>> generatePosterContent(@Valid @RequestBody PosterContentCreateRequest request) {
        PosterContentCreateResponse response = posterContentUseCase.generatePosterContent(request);
        return ResponseEntity.ok(ApiResponse.success(response, "포스터 콘텐츠가 성공적으로 생성되었습니다."));
    }

    /**
     * 홍보 포스터 저장
     * 
     * @param request 포스터 콘텐츠 저장 요청
     * @return 저장 성공 응답
     */
    @Operation(summary = "홍보 포스터 저장", description = "생성된 홍보 포스터를 저장합니다.")
    @PostMapping("/poster/save")
    public ResponseEntity<ApiResponse<Void>> savePosterContent(@Valid @RequestBody PosterContentSaveRequest request) {
        posterContentUseCase.savePosterContent(request);
        return ResponseEntity.ok(ApiResponse.success(null, "포스터 콘텐츠가 성공적으로 저장되었습니다."));
    }

    /**
     * 콘텐츠 수정
     * 
     * @param contentId 수정할 콘텐츠 ID
     * @param request 콘텐츠 수정 요청
     * @return 수정된 콘텐츠 정보
     */
    @Operation(summary = "콘텐츠 수정", description = "기존 콘텐츠를 수정합니다.")
    @PutMapping("/{contentId}")
    public ResponseEntity<ApiResponse<ContentUpdateResponse>> updateContent(
            @Parameter(description = "콘텐츠 ID", required = true)
            @PathVariable Long contentId,
            @Valid @RequestBody ContentUpdateRequest request) {
        ContentUpdateResponse response = contentQueryUseCase.updateContent(contentId, request);
        return ResponseEntity.ok(ApiResponse.success(response, "콘텐츠가 성공적으로 수정되었습니다."));
    }

    /**
     * 콘텐츠 목록 조회
     * 
     * @param contentType 콘텐츠 타입 필터
     * @param platform 플랫폼 필터
     * @param period 기간 필터
     * @param sortBy 정렬 기준
     * @return 콘텐츠 목록
     */
    @Operation(summary = "콘텐츠 목록 조회", description = "다양한 필터와 정렬 옵션으로 콘텐츠 목록을 조회합니다.")
    @GetMapping
    public ResponseEntity<ApiResponse<List<ContentResponse>>> getContents(
            @Parameter(description = "콘텐츠 타입")
            @RequestParam(required = false) String contentType,
            @Parameter(description = "플랫폼")
            @RequestParam(required = false) String platform,
            @Parameter(description = "기간")
            @RequestParam(required = false) String period,
            @Parameter(description = "정렬 기준")
            @RequestParam(required = false) String sortBy) {
        List<ContentResponse> response = contentQueryUseCase.getContents(contentType, platform, period, sortBy);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    /**
     * 진행 중인 콘텐츠 목록 조회
     * 
     * @param period 기간 필터
     * @return 진행 중인 콘텐츠 목록
     */
    @Operation(summary = "진행 콘텐츠 조회", description = "현재 진행 중인 콘텐츠 목록을 조회합니다.")
    @GetMapping("/ongoing")
    public ResponseEntity<ApiResponse<List<OngoingContentResponse>>> getOngoingContents(
            @Parameter(description = "기간")
            @RequestParam(required = false) String period) {
        List<OngoingContentResponse> response = contentQueryUseCase.getOngoingContents(period);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    /**
     * 콘텐츠 상세 조회
     * 
     * @param contentId 조회할 콘텐츠 ID
     * @return 콘텐츠 상세 정보
     */
    @Operation(summary = "콘텐츠 상세 조회", description = "특정 콘텐츠의 상세 정보를 조회합니다.")
    @GetMapping("/{contentId}")
    public ResponseEntity<ApiResponse<ContentDetailResponse>> getContentDetail(
            @Parameter(description = "콘텐츠 ID", required = true)
            @PathVariable Long contentId) {
        ContentDetailResponse response = contentQueryUseCase.getContentDetail(contentId);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    /**
     * 콘텐츠 삭제
     * 
     * @param contentId 삭제할 콘텐츠 ID
     * @return 삭제 성공 응답
     */
    @Operation(summary = "콘텐츠 삭제", description = "콘텐츠를 삭제합니다.")
    @DeleteMapping("/{contentId}")
    public ResponseEntity<ApiResponse<Void>> deleteContent(
            @Parameter(description = "콘텐츠 ID", required = true)
            @PathVariable Long contentId) {
        contentQueryUseCase.deleteContent(contentId);
        return ResponseEntity.ok(ApiResponse.success(null, "콘텐츠가 성공적으로 삭제되었습니다."));
    }
}
