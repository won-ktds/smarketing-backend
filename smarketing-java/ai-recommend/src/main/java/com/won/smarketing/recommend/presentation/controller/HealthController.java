//package com.won.smarketing.recommend.presentation.controller;
//
//import org.springframework.web.bind.annotation.GetMapping;
//import org.springframework.web.bind.annotation.RestController;
//
//import java.time.LocalDateTime;
//import java.util.Map;
//
///**
// * 헬스체크 컨트롤러
// */
//@RestController
//public class HealthController {
//
//    @GetMapping("/health")
//    public Map<String, Object> health() {
//        return Map.of(
//            "status", "UP",
//            "service", "ai-recommend-service",
//            "timestamp", LocalDateTime.now(),
//            "message", "AI 추천 서비스가 정상 동작 중입니다.",
//            "features", Map.of(
//                "store_integration", "매장 서비스 연동",
//                "python_ai_integration", "Python AI 서비스 연동",
//                "fallback_support", "Fallback 팁 생성 지원"
//            )
//        );
//    }
//}
//            }
//
//        } catch (Exception e) {
//            log.error("매장 정보 조회 실패, Mock 데이터 반환: storeId={}", storeId, e);
//            return createMockStoreData(storeId);