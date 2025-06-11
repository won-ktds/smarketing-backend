package com.won.smarketing.recommend.domain.repository;

import com.won.smarketing.recommend.domain.model.MarketingTip;
import com.won.smarketing.recommend.domain.model.TipId;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

/**
 * 마케팅 팁 저장소 인터페이스
 * 마케팅 팁 도메인의 데이터 접근 추상화
 */
public interface MarketingTipRepository {
    
    /**
     * 마케팅 팁 저장
     * 
     * @param marketingTip 저장할 마케팅 팁
     * @return 저장된 마케팅 팁
     */
    MarketingTip save(MarketingTip marketingTip);
    
    /**
     * 마케팅 팁 ID로 조회
     * 
     * @param id 마케팅 팁 ID
     * @return 마케팅 팁 (Optional)
     */
    Optional<MarketingTip> findById(TipId id);
    
    /**
     * 매장별 마케팅 팁 목록 조회
     * 
     * @param storeId 매장 ID
     * @return 마케팅 팁 목록
     */
    List<MarketingTip> findByStoreId(Long storeId);
    
    /**
     * 특정 기간 내 생성된 마케팅 팁 조회
     * 
     * @param storeId 매장 ID
     * @param startDate 시작 시각
     * @param endDate 종료 시각
     * @return 마케팅 팁 목록
     */
    List<MarketingTip> findByStoreIdAndCreatedAtBetween(Long storeId, LocalDateTime startDate, LocalDateTime endDate);
    
    /**
     * 마케팅 팁 삭제
     * 
     * @param id 삭제할 마케팅 팁 ID
     */
    void deleteById(TipId id);
}
