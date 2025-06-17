package com.won.smarketing.store.repository;

import com.won.smarketing.store.entity.Menu;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Objects;
import java.util.Optional;

/**
 * 메뉴 정보 데이터 접근을 위한 Repository
 * JPA를 사용한 메뉴 CRUD 작업 처리
 */
@Repository
public interface MenuRepository extends JpaRepository<Menu, Long> {
//    /**
//     * 전체 메뉴 조회 (메뉴명 오름차순)
//     *
//     * @return 메뉴 목록
//     */
//    List<Menu> findAllByOrderByMenuNameAsc(Long );
    
    /**
     * 매장별 메뉴 조회
     * 
     * @param storeId 매장 ID
     * @return 메뉴 목록
     */
    List<Menu> findByStoreId(Long storeId);
}
