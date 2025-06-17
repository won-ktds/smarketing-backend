// store/src/main/java/com/won/smarketing/store/dto/ImageUploadResponse.java
package com.won.smarketing.store.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 이미지 업로드 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "이미지 업로드 응답")
public class ImageUploadResponse {

    @Schema(description = "업로드된 이미지 URL", example = "https://storage.blob.core.windows.net/menu-images/menu_123_20241201_143000_abc12345.jpg")
    private String imageUrl;

    @Schema(description = "원본 파일명", example = "americano.jpg")
    private String originalFileName;

    @Schema(description = "저장된 파일명", example = "menu_123_20241201_143000_abc12345.jpg")
    private String savedFileName;

    @Schema(description = "파일 크기 (바이트)", example = "1024000")
    private Long fileSize;

    @Schema(description = "업로드 성공 여부", example = "true")
    private boolean success;

    @Schema(description = "메시지", example = "이미지 업로드가 완료되었습니다.")
    private String message;
}