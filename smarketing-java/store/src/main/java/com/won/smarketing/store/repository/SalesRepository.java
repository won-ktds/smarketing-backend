package com.won.smarketing.store.repository;

import com.won.smarketing.store.entity.Sales;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

/**
 * 매출 정보 데이터 접근을 위한 Repository
 * JPA를 사용한 매출 조회 작업 처리
 */
@Repository
public interface SalesRepository extends JpaRepository<Sales, Long> {

    /**
     * 매장의 특정 날짜 매출 조회
     *
     * @param storeId 매장 ID
     * @param salesDate 매출 날짜
     * @return 해당 날짜 매출 목록
     */
    List<Sales> findByStoreIdAndSalesDate(Long storeId, LocalDate salesDate);

    /**
     * 매장의 특정 기간 매출 조회
     *
     * @param storeId 매장 ID
     * @param startDate 시작 날짜
     * @param endDate 종료 날짜
     * @return 해당 기간 매출 목록
     */
    List<Sales> findByStoreIdAndSalesDateBetween(Long storeId, LocalDate startDate, LocalDate endDate);

    /**
     * 매장의 오늘 매출 조회 (네이티브 쿼리)
     *
     * @param storeId 매장 ID
     * @return 오늘 매출
     */
    @Query(value = "SELECT COALESCE(SUM(sales_amount), 0) FROM sales WHERE store_id = :storeId AND sales_date = CURRENT_DATE", nativeQuery = true)
    BigDecimal findTodaySalesByStoreIdNative(@Param("storeId") Long storeId);

    /**
     * 매장의 어제 매출 조회 (네이티브 쿼리)
     *
     * @param storeId 매장 ID
     * @return 어제 매출
     */
    @Query(value = "SELECT COALESCE(SUM(sales_amount), 0) FROM sales WHERE store_id = :storeId AND sales_date = CURRENT_DATE - INTERVAL '1 day'", nativeQuery = true)
    BigDecimal findYesterdaySalesByStoreIdNative(@Param("storeId") Long storeId);

    /**
     * 매장의 이번 달 매출 조회 (네이티브 쿼리)
     *
     * @param storeId 매장 ID
     * @return 이번 달 매출
     */
    @Query(value = "SELECT COALESCE(SUM(sales_amount), 0) FROM sales WHERE store_id = :storeId " +
            "AND EXTRACT(YEAR FROM sales_date) = EXTRACT(YEAR FROM CURRENT_DATE) " +
            "AND EXTRACT(MONTH FROM sales_date) = EXTRACT(MONTH FROM CURRENT_DATE)", nativeQuery = true)
    BigDecimal findMonthSalesByStoreIdNative(@Param("storeId") Long storeId);
}