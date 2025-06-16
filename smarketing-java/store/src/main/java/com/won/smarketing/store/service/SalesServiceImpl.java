package com.won.smarketing.store.service;

import com.won.smarketing.store.dto.SalesResponse;
import com.won.smarketing.store.entity.Sales;
import com.won.smarketing.store.repository.SalesRepository;
import com.won.smarketing.store.repository.StoreRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.stream.Collectors;

/**
 * 매출 관리 서비스 구현체
 * 매출 조회 기능 구현
 */
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class SalesServiceImpl implements SalesService {

    private final SalesRepository salesRepository;

    /**
     * 매출 정보 조회
     *
     * @return 매출 정보 (오늘, 월간, 전일 대비)
     */
    @Override
    public SalesResponse getSales(Long storeId) {
        // 오늘 매출 계산
        BigDecimal todaySales = calculateSalesByDate(storeId, LocalDate.now());

        // 이번 달 매출 계산
        BigDecimal monthSales = calculateMonthSales(storeId);

        // 어제 매출 계산
        BigDecimal yesterdaySales = calculateSalesByDate(storeId, LocalDate.now().minusDays(1));

        // 전일 대비 매출 변화량 계산
        BigDecimal previousDayComparison = todaySales.subtract(yesterdaySales);

        //오늘로부터 1년 전까지의 매출 리스트

        return SalesResponse.builder()
                .todaySales(todaySales)
                .monthSales(monthSales)
                .yearSales(getSalesAmountListLast365Days(storeId))
                .previousDayComparison(previousDayComparison)
                .build();
    }

    /**
     * 특정 날짜의 매출 계산
     *
     * @param storeId 매장 ID
     * @param date 날짜
     * @return 해당 날짜 매출
     */
    private BigDecimal calculateSalesByDate(Long storeId, LocalDate date) {
        List<Sales> salesList = salesRepository.findByStoreIdAndSalesDate(storeId, date);
        return salesList.stream()
                .map(Sales::getSalesAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }

    /**
     * 이번 달 매출 계산
     *
     * @param storeId 매장 ID
     * @return 이번 달 매출
     */
    private BigDecimal calculateMonthSales(Long storeId) {
        LocalDate now = LocalDate.now();
        LocalDate startOfMonth = now.withDayOfMonth(1);
        LocalDate endOfMonth = now.withDayOfMonth(now.lengthOfMonth());

        List<Sales> salesList = salesRepository.findByStoreIdAndSalesDateBetween(storeId, startOfMonth, endOfMonth);
        return salesList.stream()
                .map(Sales::getSalesAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }

    /**
     * 최근 365일 매출 금액 리스트 조회
     *
     * @param storeId 매장 ID
     * @return 최근 365일 매출 금액 리스트
     */
    private List<Sales> getSalesAmountListLast365Days(Long storeId) {
        LocalDate endDate = LocalDate.now();
        LocalDate startDate = endDate.minusDays(365);

        // Sales 엔티티 전체를 조회하는 메서드 사용
       return salesRepository.findSalesDataLast365Days(storeId, startDate, endDate);
    }
}