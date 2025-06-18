// store/src/main/java/com/won/smarketing/store/service/BlobStorageServiceImpl.java
package com.won.smarketing.content.domain.service;

import com.azure.core.util.BinaryData;
import com.azure.storage.blob.BlobClient;
import com.azure.storage.blob.BlobContainerClient;
import com.azure.storage.blob.BlobServiceClient;
import com.azure.storage.blob.models.BlobHttpHeaders;
import com.azure.storage.blob.models.PublicAccessType;
import com.won.smarketing.common.exception.BusinessException;
import com.won.smarketing.common.exception.ErrorCode;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;

/**
 * Azure Blob Storage 서비스 구현체
 * 이미지 파일 업로드, 삭제 기능 구현
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class BlobStorageServiceImpl implements BlobStorageService {

    private final BlobServiceClient blobServiceClient;

    @Value("${azure.storage.max-file-size:10485760}") // 10MB
    private long maxFileSize;

    // 허용되는 이미지 확장자
    private static final List<String> ALLOWED_EXTENSIONS = Arrays.asList(
            "jpg", "jpeg", "png", "gif", "bmp", "webp"
    );

    // 허용되는 MIME 타입
    private static final List<String> ALLOWED_MIME_TYPES = Arrays.asList(
            "image/jpeg", "image/png", "image/gif", "image/bmp", "image/webp"
    );

    /**
     * 이미지 파일 업로드
     *
     * @param files 업로드할 파일들
     * @return 업로드된 파일의 URL
     */
    @Override
    public List<String> uploadImage(List<MultipartFile> files, String containerName) {
        // 파일 유효성 검증
        validateImageFile(files);
        List<String> urls = new ArrayList<>();

        try {
            // 컨테이너 존재 확인 및 생성
            for(MultipartFile file : files) {
                String fileName = generateMenuImageFileName(file.getOriginalFilename());

                ensureContainerExists(containerName);

                // Blob 클라이언트 생성
                BlobContainerClient containerClient = blobServiceClient.getBlobContainerClient(containerName);
                BlobClient blobClient = containerClient.getBlobClient(fileName);

                // 파일 업로드 (간단한 방식)
                BinaryData binaryData = BinaryData.fromBytes(file.getBytes());

                // 파일 업로드 실행 (덮어쓰기 허용)
                blobClient.upload(binaryData, true);

                // Content-Type 설정
                BlobHttpHeaders headers = new BlobHttpHeaders().setContentType(file.getContentType());
                blobClient.setHttpHeaders(headers);

                String fileUrl = blobClient.getBlobUrl();
                log.info("이미지 업로드 성공: {}", fileUrl);

                urls.add(fileUrl);
            }
            return urls;

        } catch (IOException e) {
            log.error("이미지 업로드 실패 - 파일 읽기 오류: {}", e.getMessage());
            throw new BusinessException(ErrorCode.FILE_UPLOAD_FAILED);
        } catch (Exception e) {
            log.error("이미지 업로드 실패: {}", e.getMessage());
            throw new BusinessException(ErrorCode.FILE_UPLOAD_FAILED);
        }
    }

    /**
     * 파일 삭제
     *
     * @param fileUrl 삭제할 파일의 URL
     */
//    @Override
    public void deleteFile(String fileUrl) {
        try {
            // URL에서 컨테이너명과 파일명 추출
            String[] urlParts = extractContainerAndFileName(fileUrl);
            String containerName = urlParts[0];
            String fileName = urlParts[1];

            BlobContainerClient containerClient = blobServiceClient.getBlobContainerClient(containerName);
            BlobClient blobClient = containerClient.getBlobClient(fileName);

            boolean deleted = blobClient.deleteIfExists();

            if (deleted) {
                log.info("파일 삭제 성공: {}", fileUrl);
            } else {
                log.warn("파일이 존재하지 않음: {}", fileUrl);
            }

        } catch (Exception e) {
            log.error("파일 삭제 실패: {}", e.getMessage());
        }
    }

    /**
     * 컨테이너 존재 여부 확인 및 생성
     *
     * @param containerName 컨테이너 이름
     */
    @Override
    public void ensureContainerExists(String containerName) {
        try {
            BlobContainerClient containerClient = blobServiceClient.getBlobContainerClient(containerName);

            if (!containerClient.exists()) {
                containerClient.createWithResponse(null, PublicAccessType.BLOB, null, null);
                log.info("컨테이너 생성 완료: {}", containerName);
            }

        } catch (Exception e) {
            log.error("컨테이너 생성 실패: {}", e.getMessage());
            throw new BusinessException(ErrorCode.STORAGE_CONTAINER_ERROR);
        }
    }

    /**
     * 이미지 파일 유효성 검증
     *
     * @param files 검증할 파일
     */
    private void validateImageFile(List<MultipartFile> files) {
        // 파일 존재 여부 확인
        if (files == null || files.isEmpty()) {
            throw new BusinessException(ErrorCode.FILE_NOT_FOUND);
        }

        for (MultipartFile file : files) {
            // 파일 크기 확인
            if (file.getSize() > maxFileSize) {
                throw new BusinessException(ErrorCode.FILE_SIZE_EXCEEDED);
            }

            // 파일 확장자 확인
            String originalFilename = file.getOriginalFilename();
            if (originalFilename == null) {
                throw new BusinessException(ErrorCode.INVALID_FILE_NAME);
            }

            String extension = getFileExtension(originalFilename).toLowerCase();
            if (!ALLOWED_EXTENSIONS.contains(extension)) {
                throw new BusinessException(ErrorCode.INVALID_FILE_EXTENSION);
            }

            // MIME 타입 확인
            String contentType = file.getContentType();
            if (contentType == null || !ALLOWED_MIME_TYPES.contains(contentType)) {
                throw new BusinessException(ErrorCode.INVALID_FILE_TYPE);
            }
        }
    }

    /**
     * 메뉴 이미지 파일명 생성
     *
     * @param originalFilename 원본 파일명
     * @return 생성된 파일명
     */
    private String generateMenuImageFileName(String originalFilename) {
        String extension = getFileExtension(originalFilename);
        String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
        String uuid = UUID.randomUUID().toString().substring(0, 8);

        return String.format("menu_%s_%s.%s", timestamp, uuid, extension);
    }

    /**
     * 매장 이미지 파일명 생성
     *
     * @param storeId 매장 ID
     * @param originalFilename 원본 파일명
     * @return 생성된 파일명
     */
    private String generateStoreImageFileName(Long storeId, String originalFilename) {
        String extension = getFileExtension(originalFilename);
        String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
        String uuid = UUID.randomUUID().toString().substring(0, 8);

        return String.format("store_%d_%s_%s.%s", storeId, timestamp, uuid, extension);
    }

    /**
     * 파일 확장자 추출
     *
     * @param filename 파일명
     * @return 확장자
     */
    private String getFileExtension(String filename) {
        int lastDotIndex = filename.lastIndexOf('.');
        if (lastDotIndex == -1) {
            return "";
        }
        return filename.substring(lastDotIndex + 1);
    }

    /**
     * URL에서 컨테이너명과 파일명 추출
     *
     * @param fileUrl 파일 URL
     * @return [컨테이너명, 파일명] 배열
     */
    private String[] extractContainerAndFileName(String fileUrl) {
        // URL 형식: https://accountname.blob.core.windows.net/container/filename
        try {
            String[] parts = fileUrl.split("/");
            String containerName = parts[parts.length - 2];
            String fileName = parts[parts.length - 1];
            return new String[]{containerName, fileName};
        } catch (Exception e) {
            throw new BusinessException(ErrorCode.INVALID_FILE_URL);
        }
    }
}