// store/src/main/java/com/won/smarketing/store/controller/ImageController.java
package com.won.smarketing.store.controller;

import com.won.smarketing.store.dto.ImageUploadResponse;
import com.won.smarketing.store.dto.MenuResponse;
import com.won.smarketing.store.dto.StoreResponse;
import com.won.smarketing.store.service.BlobStorageService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

/**
 * 이미지 업로드 API 컨트롤러
 * 메뉴 이미지, 매장 이미지 업로드 기능 제공
 */
@RestController
@RequestMapping("/api/images")
@RequiredArgsConstructor
@Slf4j
@Tag(name = "이미지 업로드 API", description = "메뉴 및 매장 이미지 업로드 관리")
public class ImageController {

    private final BlobStorageService blobStorageService;

    /**
     * 메뉴 이미지 업로드
     *
     * @param menuId 메뉴 ID
     * @param file 업로드할 이미지 파일
     * @return 업로드 결과
     */
    @PostMapping(value = "/menu/{menuId}", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    @Operation(summary = "메뉴 이미지 업로드", description = "메뉴의 이미지를 Azure Blob Storage에 업로드합니다.")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "이미지 업로드 성공",
                    content = @Content(schema = @Schema(implementation = ImageUploadResponse.class))),
            @ApiResponse(responseCode = "400", description = "잘못된 요청 (파일 형식, 크기 등)"),
            @ApiResponse(responseCode = "404", description = "메뉴를 찾을 수 없음"),
            @ApiResponse(responseCode = "500", description = "서버 오류")
    })
    public ResponseEntity<MenuResponse> uploadMenuImage(
            @Parameter(description = "메뉴 ID", required = true)
            @PathVariable Long menuId,
            @Parameter(description = "업로드할 이미지 파일", required = true)
            @RequestParam("file") MultipartFile file) {

        log.info("메뉴 이미지 업로드 요청 - 메뉴 ID: {}, 파일: {}", menuId, file.getOriginalFilename());

        MenuResponse response = blobStorageService.uploadMenuImage(file, menuId);

        return ResponseEntity.ok(response);
    }

    /**
     * 매장 이미지 업로드
     *
     * @param storeId 매장 ID
     * @param file 업로드할 이미지 파일
     * @return 업로드 결과
     */
    @PostMapping(value = "/store/{storeId}", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    @Operation(summary = "매장 이미지 업로드", description = "매장의 이미지를 Azure Blob Storage에 업로드합니다.")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "이미지 업로드 성공",
                    content = @Content(schema = @Schema(implementation = ImageUploadResponse.class))),
            @ApiResponse(responseCode = "400", description = "잘못된 요청 (파일 형식, 크기 등)"),
            @ApiResponse(responseCode = "404", description = "매장을 찾을 수 없음"),
            @ApiResponse(responseCode = "500", description = "서버 오류")
    })
    public ResponseEntity<StoreResponse> uploadStoreImage(
            @Parameter(description = "매장 ID", required = true)
            @PathVariable Long storeId,
            @Parameter(description = "업로드할 이미지 파일", required = true)
            @RequestParam("file") MultipartFile file) {

        log.info("매장 이미지 업로드 요청 - 매장 ID: {}, 파일: {}", storeId, file.getOriginalFilename());
        StoreResponse response = blobStorageService.uploadStoreImage(file, storeId);

        return ResponseEntity.ok(response);
    }

    /**
     * 이미지 삭제
     *
     * @param imageUrl 삭제할 이미지 URL
     * @return 삭제 결과
     */
    //@DeleteMapping
    //@Operation(summary = "이미지 삭제", description = "Azure Blob Storage에서 이미지를 삭제합니다.")
//    @ApiResponses(value = {
//            @ApiResponse(responseCode = "200", description = "이미지 삭제 성공"),
//            @ApiResponse(responseCode = "400", description = "잘못된 요청"),
//            @ApiResponse(responseCode = "404", description = "이미지를 찾을 수 없음"),
//            @ApiResponse(responseCode = "500", description = "서버 오류")
//    })
//    public ResponseEntity<ImageUploadResponse> deleteImage(
//            @Parameter(description = "삭제할 이미지 URL", required = true)
//            @RequestParam String imageUrl) {
//
//        log.info("이미지 삭제 요청 - URL: {}", imageUrl);
//
//        try {
//            boolean deleted = blobStorageService.deleteFile(imageUrl);
//
//            ImageUploadResponse response = ImageUploadResponse.builder()
//                    .imageUrl(imageUrl)
//                    .success(deleted)
//                    .message(deleted ? "이미지 삭제가 완료되었습니다." : "삭제할 이미지를 찾을 수 없습니다.")
//                    .build();
//
//            return ResponseEntity.ok(response);
//
//        } catch (Exception e) {
//            log.error("이미지 삭제 실패 - URL: {}", imageUrl, e);
//
//            ImageUploadResponse response = ImageUploadResponse.builder()
//                    .imageUrl(imageUrl)
//                    .success(false)
//                    .message("이미지 삭제에 실패했습니다: " + e.getMessage())
//                    .build();
//
//            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
//        }
//    }

    /**
     * URL에서 파일명 추출
     *
     * @param url 파일 URL
     * @return 파일명
     */
    private String extractFileNameFromUrl(String url) {
        if (url == null || url.isEmpty()) {
            return null;
        }

        try {
            return url.substring(url.lastIndexOf('/') + 1);
        } catch (Exception e) {
            log.warn("URL에서 파일명 추출 실패: {}", url);
            return null;
        }
    }
}