// store/src/main/java/com/won/smarketing/store/service/BlobStorageService.java
package com.won.smarketing.content.domain.service;

import org.springframework.web.multipart.MultipartFile;

import java.util.List;

/**
 * Azure Blob Storage 서비스 인터페이스
 * 파일 업로드, 다운로드, 삭제 기능 정의
 */
public interface BlobStorageService {

    /**
     * 이미지 파일 업로드
     *
     * @param file 업로드할 파일
     * @return 업로드된 파일의 URL
     */
    List<String> uploadImage(List<MultipartFile> file, String containerName);


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
