package com.won.smarketing.store.service;

import com.won.smarketing.common.exception.BusinessException;
import com.won.smarketing.common.exception.ErrorCode;
import com.won.smarketing.store.dto.MenuCreateRequest;
import com.won.smarketing.store.dto.MenuResponse;
import com.won.smarketing.store.dto.MenuUpdateRequest;
import com.won.smarketing.store.entity.Menu;
import com.won.smarketing.store.repository.MenuRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

/**
 * 메뉴 관리 서비스 구현체
 * 메뉴 등록, 조회, 수정, 삭제 기능 구현
 */
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class MenuServiceImpl implements MenuService {

    private final MenuRepository menuRepository;

    /**
     * 메뉴 정보 등록
     * 
     * @param request 메뉴 등록 요청 정보
     * @return 등록된 메뉴 정보
     */
    @Override
    @Transactional
    public MenuResponse register(MenuCreateRequest request) {
        // 메뉴 엔티티 생성 및 저장
        Menu menu = Menu.builder()
                .storeId(request.getStoreId())
                .menuName(request.getMenuName())
                .category(request.getCategory())
                .price(request.getPrice())
                .description(request.getDescription())
                .image(request.getImage())
                .build();

        Menu savedMenu = menuRepository.save(menu);
        return toMenuResponse(savedMenu);
    }

    /**
     * 메뉴 목록 조회
     * 
     * @param storeId 가게 ID
     * @return 메뉴 목록
     */
    @Override
    public List<MenuResponse> getMenus(Long storeId) {
        List<Menu> menus;

        menus = menuRepository.findByStoreId(storeId);

        return menus.stream()
                .map(this::toMenuResponse)
                .collect(Collectors.toList());
    }

    /**
     * 메뉴 정보 수정
     * 
     * @param menuId 수정할 메뉴 ID
     * @param request 메뉴 수정 요청 정보
     * @return 수정된 메뉴 정보
     */
    @Override
    @Transactional
    public MenuResponse updateMenu(Long menuId, MenuUpdateRequest request) {

        Menu menu = menuRepository.findById(menuId)
                .orElseThrow(() -> new BusinessException(ErrorCode.MENU_NOT_FOUND));

        // 메뉴 정보 업데이트
        menu.updateMenu(
                request.getMenuName(),
                request.getCategory(),
                request.getPrice(),
                request.getDescription(),
                request.getImage()
        );

        Menu updatedMenu = menuRepository.save(menu);
        return toMenuResponse(updatedMenu);
    }

    /**
     * 메뉴 삭제
     * 
     * @param menuId 삭제할 메뉴 ID
     */
    @Override
    @Transactional
    public void deleteMenu(Long menuId) {
        Menu menu = menuRepository.findById(menuId)
                .orElseThrow(() -> new BusinessException(ErrorCode.MENU_NOT_FOUND));
        
        menuRepository.delete(menu);
    }

    /**
     * Menu 엔티티를 MenuResponse DTO로 변환
     * 
     * @param menu Menu 엔티티
     * @return MenuResponse DTO
     */
    private MenuResponse toMenuResponse(Menu menu) {
        return MenuResponse.builder()
                .menuId(menu.getMenuId())
                .menuName(menu.getMenuName())
                .category(menu.getCategory())
                .price(menu.getPrice())
                .description(menu.getDescription())
                .image(menu.getImage())
                .createdAt(menu.getCreatedAt())
                .updatedAt(menu.getUpdatedAt())
                .build();
    }
}
