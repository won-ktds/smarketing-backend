package com.won.smarketing.member.service;

import com.won.smarketing.common.exception.BusinessException;
import com.won.smarketing.common.exception.ErrorCode;
import com.
재시도
Y
계속
편집
Member 인증 서비스 구현체 및 Controllers
코드 ∙ 버전 2 
       // 새로운 리프레시 토큰을 Redis에 저장
        redisTemplate.opsForValue().set(
                REFRESH_TOKEN_PREFIX + userId, 
                newRefreshToken, 
                7, 
                TimeUnit.DAYS
        );
        
        // 기존 리프레시 토큰을
Store 서비스 Entity 및 DTO 클래스들
코드 