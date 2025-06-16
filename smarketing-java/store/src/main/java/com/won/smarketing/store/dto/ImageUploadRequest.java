// store/src/main/java/com/won/smarketing/store/dto/ImageUploadRequest.java
package com.won.smarketing.store.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.web.multipart.MultipartFile;

import jakarta.validation.constraints.NotNull;

/**
 * 이미지 업로드 요청 DTO
 * 이미지 파일 업로드 시 필요한 정보를 전달합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "이미지 업로드 요청")
public class ImageUploadRequest {

    @Schema(description = "업로드할 이미지 파일", required = true)
    @NotNull(message = "이미지 파일은 필수입니다")
    private MultipartFile file;
}