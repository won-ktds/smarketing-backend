package com.won.smarketing.store.service;

import com.won.smarketing.store.dto.SalesResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * 매출 서비스 구현체
 * 매출 조회 기능 구현 (현재는 Mock 데이터)
 */
@Slf4j
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class SalesServiceImpl implements SalesService {

    /**
     * 매출 정보 조회
     * 현재는 Mock 데이터를 반환 (실제로는 매출 데이터 조회 로직 필요)
     * 
     * @return 매출 정보
     */
    @Override
    public SalesResponse getSales() {
        log.info("매출 정보 조회");
        
        // Mock 데이터 (실제로는 데이터베이스에서 조회)
        BigDecimal todaySales = new BigDecimal("150000");
        BigDecimal monthSales = new BigDecimal("4500000");
        BigDecimal yesterdaySales = new BigDecimal("125000");
        BigDecimal targetSales = new BigDecimal("176000");
        
        // 전일 대비 변화 계산
        BigDecimal previousDayComparison = todaySales.subtract(yesterdaySales);
        BigDecimal previousDayChangeRate = yesterdaySales.compareTo(BigDecimal.ZERO) > 0
                ? previousDayComparison.divide(yesterdaySales, 4, RoundingMode.HALF_UP)
                    .multiply(new BigDecimal("100"))
                : BigDecimal.ZERO;
        
        // 목표 대비 달성률 계산
        BigDecimal goalAchievementRate = targetSales.compareTo(BigDecimal.ZERO) > 0
                ? todaySales.divide(targetSales, 4, RoundingMode.HALF_UP)
                    .multiply(new BigDecimal("100"))
                : BigDecimal.ZERO;
        
        return SalesResponse.builder()
                .todaySales(todaySales)
                .monthSales(monthSales)
                .previousDayComparison(previousDayComparison)
                .previousDayChangeRate(previousDayChangeRate)
                .goalAchievementRate(goalAchievementRate)
                .build();
    }
}

