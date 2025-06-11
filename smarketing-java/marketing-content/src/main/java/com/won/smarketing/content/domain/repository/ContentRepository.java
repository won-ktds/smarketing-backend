package com.won.smarketing.content.domain.repository;

import com.won.smarketing.content.domain.model.Content;
import com.won.smarketing.content.domain.model.ContentId;
import com.won.smarketing.content.domain.model.ContentType;
import com.won.smarketing.content.domain.model.Platform;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * 콘텐츠 저장소 인터페이스
 * 콘텐츠 도메인의 데이터 접근 추상화
 */
@Repository
public interface ContentRepository {
    
    /**
     * 콘텐츠 저장
     * 
     * @param content 저장할 콘텐츠
     * @return 저장된 콘텐츠
     */
    Content save(Content content);
    
    /**
     * 콘텐츠 ID로 조회
     * 
     * @param id 콘텐츠 ID
     * @return 콘텐츠 (Optional)
     */
    Optional<Content> findById(ContentId id);
    
    /**
     * 필터 조건으로 콘텐츠 목록 조회
     * 
     * @param contentType 콘텐츠 타입
     * @param platform 플랫폼
     * @param period 기간
     * @param sortBy 정렬 기준
     * @return 콘텐츠 목록
     */
    List<Content> findByFilters(ContentType contentType, Platform platform, String period, String sortBy);
    
    /**
     * 진행 중인 콘텐츠 목록 조회
     * 
     * @param period 기간
     * @return 진행 중인 콘텐츠 목록
     */
    List<Content> findOngoingContents(String period);
    
    /**
     * 콘텐츠 삭제
     * 
     * @param id 삭제할 콘텐츠 ID
     */
    void deleteById(ContentId id);
}
