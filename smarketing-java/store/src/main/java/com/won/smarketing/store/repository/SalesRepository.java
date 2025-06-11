package com.won.smarketing.store.repository;

import com.won.smarketing.store.entity.Sales;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;

/**
 * 매출 정보 데이터 접근을 위한 Repository
 * JPA를 사용한 매출 조회 작업 처리
 */
@Repository
public interface SalesRepository extends JpaRepository<Sales, Long> {
    
    /**
     * 매장의 오늘 매출 조회
     * 
     * @param storeId 매장 ID
     * @return 오늘 매출
     */
    @Query("SELECT COALESCE(SUM(s.salesAmount), 0) FROM Sales s WHERE s.storeId = :storeId AND s.salesDate = CURRENT_DATE")
    BigDecimal findTodaySalesByStoreId(@Param("storeId") Long storeId);
    
    /**
     * 매장의 이번 달 매출 조회
     * 
     * @param storeId 매장 ID
     * @return 이번 달 매출
     */
    @Query("SELECT COALESCE(SUM(s.salesAmount), 0) FROM Sales s WHERE s.storeId = :storeId AND YEAR(s.salesDate) = YEAR(CURRENT_DATE) AND MONTH(s.salesDate) = MONTH(CURRENT_DATE)")
    BigDecimal findMonthSalesByStoreId(@Param("storeId") Long storeId);
    
    /**
     * 매장의 전일 대비 매출 변화량 조회
     * 
     * @param storeId 매장 ID
     * @return 전일 대비 매출 변화량
     */
    @Query("SELECT COALESCE((SELECT SUM(s1.salesAmount) FROM Sales s1 WHERE s1.storeId = :storeId AND s1.salesDate = CURRENT_DATE) - (SELECT SUM(s2.salesAmount) FROM Sales s2 WHERE s2.storeId = :storeId AND s2.salesDate = CURRENT_DATE - 1), 0)")
    BigDecimal findPreviousDayComparisonByStoreId(@Param("storeId") Long storeId);
}
