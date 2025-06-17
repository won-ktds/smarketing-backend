// marketing-content/src/main/java/com/won/smarketing/content/domain/repository/ContentRepository.java
package com.won.smarketing.content.domain.repository;

import com.won.smarketing.content.domain.model.Content;
import com.won.smarketing.content.domain.model.ContentId;
import com.won.smarketing.content.domain.model.ContentType;
import com.won.smarketing.content.domain.model.Platform;

import java.util.List;
import java.util.Optional;

/**
 * 콘텐츠 리포지토리 인터페이스
 * Clean Architecture의 Domain Layer에서 데이터 접근 정의
 */
public interface ContentRepository {

    /**
     * 콘텐츠 저장
     * @param content 저장할 콘텐츠
     * @return 저장된 콘텐츠
     */
    Content save(Content content);

    /**
     * ID로 콘텐츠 조회
     * @param id 콘텐츠 ID
     * @return 조회된 콘텐츠
     */
    Optional<Content> findById(ContentId id);

    /**
     * 필터 조건으로 콘텐츠 목록 조회
     * @param storeId 콘텐츠 타입
     * @param platform 플랫폼

     * @return 콘텐츠 목록
     */
    List<Content> findByFilters(Long storeId, Platform platform);

    /**
     * 진행 중인 콘텐츠 목록 조회
     * @param period 기간
     * @return 진행 중인 콘텐츠 목록
     */
    List<Content> findOngoingContents(String period);

    /**
     * ID로 콘텐츠 삭제
     * @param id 삭제할 콘텐츠 ID
     */
    void deleteById(ContentId id);
}