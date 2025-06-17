//import com.azure.messaging.eventhubs.EventData;
//import com.azure.messaging.eventhubs.EventHubProducerClient;
//import com.fasterxml.jackson.core.JsonProcessingException;
//import com.fasterxml.jackson.databind.ObjectMapper;
//import com.won.smarketing.recommend.domain.event.MarketingTipRequestEvent;
//import lombok.RequiredArgsConstructor;
//import lombok.extern.slf4j.Slf4j;
//import org.springframework.stereotype.Service;
//
//import java.util.UUID;
//
///**
// * 마케팅 팁 이벤트 발행자
// */
//@Slf4j
//@Service
//@RequiredArgsConstructor
//public class MarketingTipEventPublisher {
//
//    private final EventHubProducerClient producerClient;
//    private final ObjectMapper objectMapper;
//
//    public String publishMarketingTipRequest(MarketingTipRequestEvent event) {
//        try {
//            String requestId = UUID.randomUUID().toString();
//            event.setRequestId(requestId);
//
//            String eventData = objectMapper.writeValueAsString(event);
//
//            producerClient.send(EventData.create(eventData));
//
//            log.info("마케팅 팁 요청 이벤트 발행 완료: requestId={}", requestId);
//            return requestId;
//
//        } catch (JsonProcessingException e) {
//            log.error("마케팅 팁 이벤트 직렬화 실패", e);
//            throw new RuntimeException("이벤트 발행 실패", e);
//        } catch (Exception e) {
//            log.error("마케팅 팁 이벤트 발행 실패", e);
//            throw new RuntimeException("이벤트 발행 실패", e);
//        }
//    }
//}