package com.won.smarketing.store.service;

import com.won.smarketing.store.dto.SalesResponse;
import com.won.smarketing.store.repository.SalesRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;

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
        
        BigDecimal todaySales = salesRepository.findTodaySalesByStoreId(storeId);
        BigDecimal monthSales = salesRepository.findMonthSalesByStoreId(storeId);
        BigDecimal previousDayComparison = salesRepository.findPreviousDayComparisonByStoreId(storeId);

        return SalesResponse.builder()
                .todaySales(todaySales != null ? todaySales : BigDecimal.ZERO)
                .monthSales(monthSales != null ? monthSales : BigDecimal.ZERO)
                .previousDayComparison(previousDayComparison != null ? previousDayComparison : BigDecimal.ZERO)
                .build();
    }
}
