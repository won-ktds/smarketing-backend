//package com.won.smarketing.recommend.infrastructure.event;
//
//import com.azure.messaging.eventhubs.EventData;
//import com.azure.messaging.eventhubs.models.EventContext;
//import com.fasterxml.jackson.databind.ObjectMapper;
//import com.won.smarketing.recommend.domain.event.MarketingTipRequestEvent;
//import com.won.smarketing.recommend.domain.repository.MarketingTipRepository;
//import com.won.smarketing.recommend.infrastructure.external.PythonMarketingTipGenerator;
//import com.won.smarketing.recommend.infrastructure.persistence.MarketingTipEntity;
//import lombok.RequiredArgsConstructor;
//import lombok.extern.slf4j.Slf4j;
//import org.springframework.beans.factory.annotation.Value;
//import org.springframework.stereotype.Service;
//
//import java.time.LocalDateTime;
//
///**
// * 마케팅 팁 이벤트 소비자
// */
//@Slf4j
//@Service
//@RequiredArgsConstructor
//public class MarketingTipEventConsumer {
//
//    private final ObjectMapper objectMapper;
//    private final PythonMarketingTipGenerator pythonMarketingTipGenerator;
//    private final MarketingTipRepository marketingTipRepository;
//
//    @Value("${azure.eventhub.marketing-tip-hub}")
//    private String marketingTipHub;
//
//    /**
//     * Azure Event Hub 이벤트 처리
//     */
//    public void processMarketingTipRequest(EventContext eventContext) {
//        try {
//            EventData eventData = eventContext.getEventData();
//            String eventBody = eventData.getBodyAsString();
//
//            MarketingTipRequestEvent request = objectMapper.readValue(eventBody, MarketingTipRequestEvent.class);
//
//            log.info("마케팅 팁 요청 처리 시작: requestId={}", request.getRequestId());
//
//            // 상태를 PROCESSING으로 업데이트
//            updateProcessingStatus(request.getRequestId(), MarketingTipEntity.ProcessingStatus.PROCESSING);
//
//            // AI 마케팅 팁 생성
//            String marketingTip = generateMarketingTip(request);
//
//            // 완료 처리
//            completeMarketingTip(request.getRequestId(), marketingTip);
//
//            // 체크포인트 설정
//            eventContext.updateCheckpoint();
//
//            log.info("마케팅 팁 요청 처리 완료: requestId={}", request.getRequestId());
//
//        } catch (Exception e) {
//            log.error("마케팅 팁 요청 처리 실패", e);
//            handleProcessingError(eventContext, e);
//        }
//    }
//
//    private void updateProcessingStatus(String requestId, MarketingTipEntity.ProcessingStatus status) {
//        marketingTipRepository.findByRequestId(requestId)
//                .ifPresent(entity -> {
//                    entity.setStatus(status);
//                    if (status == MarketingTipEntity.ProcessingStatus.PROCESSING) {
//                        entity.setUpdatedAt(LocalDateTime.now());
//                    }
//                    marketingTipRepository.save(entity);
//                });
//    }
//
//    private String generateMarketingTip(MarketingTipRequestEvent request) {
//        // StoreWithMenuData 객체 생성 로직
//        // Python AI 서비스 호출
//        return pythonMarketingTipGenerator.generateTipFromEvent(request);
//    }
//
//    private void completeMarketingTip(String requestId, String tipContent) {
//        marketingTipRepository.findByRequestId(requestId)
//                .ifPresent(entity -> {
//                    entity.setStatus(MarketingTipEntity.ProcessingStatus.COMPLETED);
//                    entity.setTipContent(tipContent);
//                    entity.setCompletedAt(LocalDateTime.now());
//
//                    // 처리 시간 계산
//                    if (entity.getCreatedAt() != null) {
//                        long processingTime = java.time.Duration.between(
//                                entity.getCreatedAt(), LocalDateTime.now()).getSeconds();
//                        entity.setProcessingTimeSeconds((int) processingTime);
//                    }
//
//                    marketingTipRepository.save(entity);
//                });
//    }
//
//    private void handleProcessingError(EventContext eventContext, Exception e) {
//        try {
//            EventData eventData = eventContext.getEventData();
//            String eventBody = eventData.getBodyAsString();
//            MarketingTipRequestEvent request = objectMapper.readValue(eventBody, MarketingTipRequestEvent.class);
//
//            // 실패 상태로 업데이트
//            marketingTipRepository.findByRequestId(request.getRequestId())
//                    .ifPresent(entity -> {
//                        entity.setStatus(MarketingTipEntity.ProcessingStatus.FAILED);
//                        entity.setErrorMessage(e.getMessage());
//                        marketingTipRepository.save(entity);
//                    });
//
//        } catch (Exception ex) {
//            log.error("오류 처리 중 추가 오류 발생", ex);
//        }
//    }
//}