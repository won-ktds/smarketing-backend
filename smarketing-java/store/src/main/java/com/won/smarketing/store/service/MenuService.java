package com.won.smarketing.store.service;

import com.won.smarketing.store.dto.ImageUploadResponse;
import com.won.smarketing.store.dto.MenuCreateRequest;
import com.won.smarketing.store.dto.MenuResponse;
import com.won.smarketing.store.dto.MenuUpdateRequest;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

/**
 * 메뉴 서비스 인터페이스
 * 메뉴 관리 관련 비즈니스 로직 정의
 */
public interface MenuService {
    
    /**
     * 메뉴 등록
     * 
     * @param request 메뉴 등록 요청 정보
     * @return 등록된 메뉴 정보
     */
    MenuResponse register(MenuCreateRequest request);
    
    /**
     * 메뉴 목록 조회
     * 
     * @param storeId 가게 ID
     * @return 메뉴 목록
     */
    List<MenuResponse> getMenus(Long storeId);
    
    /**
     * 메뉴 정보 수정
     * 
     * @param menuId 메뉴 ID
     * @param request 메뉴 수정 요청 정보
     * @return 수정된 메뉴 정보
     */
    MenuResponse updateMenu(Long menuId, MenuUpdateRequest request);
    
    /**
     * 메뉴 삭제
     * 
     * @param menuId 메뉴 ID
     */
    void deleteMenu(Long menuId);

//    /**
//     * 메뉴 이미지 업로드
//     *
//     * @param menuId 메뉴 ID
//     * @param file 업로드할 이미지 파일
//     * @return 이미지 업로드 결과
//     */
//    ImageUploadResponse uploadMenuImage(Long menuId, MultipartFile file);
}
