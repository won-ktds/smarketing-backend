package com.won.smarketing.store.repository;

import com.won.smarketing.store.entity.Menu;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * 메뉴 정보 데이터 접근을 위한 Repository
 * JPA를 사용한 메뉴 CRUD 작업 처리
 */
@Repository
public interface MenuRepository extends JpaRepository<Menu, Long> {
    
    /**
     * 카테고리별 메뉴 조회 (메뉴명 오름차순)
     * 
     * @param category 메뉴 카테고리
     * @return 메뉴 목록
     */
    List<Menu> findByCategoryOrderByMenuNameAsc(String category);
    
    /**
     * 전체 메뉴 조회 (메뉴명 오름차순)
     * 
     * @return 메뉴 목록
     */
    List<Menu> findAllByOrderByMenuNameAsc();
    
    /**
     * 매장별 메뉴 조회
     * 
     * @param storeId 매장 ID
     * @return 메뉴 목록
     */
    List<Menu> findByStoreId(Long storeId);
}
