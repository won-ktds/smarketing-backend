package com.won.smarketing.store.service;

import com.won.smarketing.store.dto.MenuCreateRequest;
import com.won.smarketing.store.dto.MenuResponse;
import com.won.smarketing.store.dto.MenuUpdateRequest;

import java.util.List;

/**
 * 메뉴 관리 서비스 인터페이스
 * 메뉴 등록, 조회, 수정, 삭제 기능 정의
 */
public interface MenuService {
    
    /**
     * 메뉴 정보 등록
     * 
     * @param request 메뉴 등록 요청 정보
     * @return 등록된 메뉴 정보
     */
    MenuResponse register(MenuCreateRequest request);
    
    /**
     * 메뉴 목록 조회
     * 
     * @param category 메뉴 카테고리 (선택사항)
     * @return 메뉴 목록
     */
    List<MenuResponse> getMenus(String category);
    
    /**
     * 메뉴 정보 수정
     * 
     * @param menuId 수정할 메뉴 ID
     * @param request 메뉴 수정 요청 정보
     * @return 수정된 메뉴 정보
     */
    MenuResponse updateMenu(Long menuId, MenuUpdateRequest request);
    
    /**
     * 메뉴 삭제
     * 
     * @param menuId 삭제할 메뉴 ID
     */
    void deleteMenu(Long menuId);
}
