// store/src/main/java/com/won/smarketing/store/service/BlobStorageService.java
package com.won.smarketing.store.service;

import com.won.smarketing.store.dto.MenuResponse;
import com.won.smarketing.store.dto.StoreResponse;
import org.springframework.web.multipart.MultipartFile;

/**
 * Azure Blob Storage 서비스 인터페이스
 * 파일 업로드, 다운로드, 삭제 기능 정의
 */
public interface BlobStorageService {

    /**
     * 이미지 파일 업로드
     *
     * @param file 업로드할 파일
     * @param containerName 컨테이너 이름
     * @param fileName 저장할 파일명
     * @return 업로드된 파일의 URL
     */
    String uploadImage(MultipartFile file, String containerName, String fileName);

    /**
     * 메뉴 이미지 업로드 (편의 메서드)
     *
     * @param file 업로드할 파일
     * @return 업로드된 파일의 URL
     */
    MenuResponse uploadMenuImage(MultipartFile file, Long menuId);

    /**
     * 매장 이미지 업로드 (편의 메서드)
     *
     * @param file 업로드할 파일
     * @param storeId 매장 ID
     * @return 업로드된 파일의 URL
     */
    StoreResponse uploadStoreImage(MultipartFile file, Long storeId);

    /**
     * 파일 삭제
     *
     * @param fileUrl 삭제할 파일의 URL
     * @return 삭제 성공 여부
     */
    //boolean deleteFile(String fileUrl);

    /**
     * 컨테이너 존재 여부 확인 및 생성
     *
     * @param containerName 컨테이너 이름
     */
    void ensureContainerExists(String containerName);
}
