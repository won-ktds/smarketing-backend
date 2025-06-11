package com.won.smarketing.store.service;

import com.won.smarketing.store.dto.SalesResponse;
import com.won.smarketing.store.entity.Sales;
import com.won.smarketing.store.repository.SalesRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

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
    public SalesResponse getSales() {
        // TODO: 현재는 더미 데이터 반환, 실제로는 현재 로그인한 사용자의 매장 ID를 사용해야 함
        Long storeId = 1L; // 임시로 설정

        // 오늘 매출 계산
        BigDecimal todaySales = calculateSalesByDate(storeId, LocalDate.now());

        // 이번 달 매출 계산
        BigDecimal monthSales = calculateMonthSales(storeId);

        // 어제 매출 계산
        BigDecimal yesterdaySales = calculateSalesByDate(storeId, LocalDate.now().minusDays(1));

        // 전일 대비 매출 변화량 계산
        BigDecimal previousDayComparison = todaySales.subtract(yesterdaySales);

        return SalesResponse.builder()
                .todaySales(todaySales)
                .monthSales(monthSales)
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
}