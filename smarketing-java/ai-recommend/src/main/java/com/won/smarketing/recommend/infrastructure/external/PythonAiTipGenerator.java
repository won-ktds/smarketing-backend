import com.won.smarketing.recommend.domain.model.StoreData;
import com.won.smarketing.recommend.domain.model.WeatherData;
import com.won.smarketing.recommend.domain.service.AiTipGenerator;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.Duration;
import java.util.Map;

/**
 * Python AI 팁 생성 구현체
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class PythonAiTipGenerator implements AiTipGenerator {

    private final WebClient webClient;

    @Value("${external.python-ai-service.base-url}")
    private String pythonAiServiceBaseUrl;

    @Value("${external.python-ai-service.api-key}")
    private String pythonAiServiceApiKey;

    @Value("${external.python-ai-service.timeout}")
    private int timeout;

    @Override
    public String generateTip(StoreData storeData, WeatherData weatherData, String additionalRequirement) {
        try {
            log.debug("Python AI 서비스 호출: store={}, weather={}도",
                    storeData.getStoreName(), weatherData.getTemperature());

            // Python AI 서비스 사용 가능 여부 확인
            if (isPythonServiceAvailable()) {
                return callPythonAiService(storeData, weatherData, additionalRequirement);
            } else {
                log.warn("Python AI 서비스 사용 불가, Fallback 처리");
                return createFallbackTip(storeData, weatherData, additionalRequirement);
            }

        } catch (Exception e) {
            log.error("Python AI 서비스 호출 실패, Fallback 처리: {}", e.getMessage());
            return createFallbackTip(storeData, weatherData, additionalRequirement);
        }
    }

    private boolean isPythonServiceAvailable() {
        return !pythonAiServiceApiKey.equals("dummy-key");
    }

    private String callPythonAiService(StoreData storeData, WeatherData weatherData, String additionalRequirement) {
        try {
            Map<String, Object> requestData = Map.of(
                    "store_name", storeData.getStoreName(),
                    "business_type", storeData.getBusinessType(),
                    "location", storeData.getLocation(),
                    "temperature", weatherData.getTemperature(),
                    "weather_condition", weatherData.getCondition(),
                    "humidity", weatherData.getHumidity(),
                    "additional_requirement", additionalRequirement != null ? additionalRequirement : ""
            );

            PythonAiResponse response = webClient
                    .post()
                    .uri(pythonAiServiceBaseUrl + "/api/v1/generate-marketing-tip")
                    .header("Authorization", "Bearer " + pythonAiServiceApiKey)
                    .header("Content-Type", "application/json")
                    .bodyValue(requestData)
                    .retrieve()
                    .bodyToMono(PythonAiResponse.class)
                    .timeout(Duration.ofMillis(timeout))
                    .block();

            if (response != null && response.getTip() != null && !response.getTip().trim().isEmpty()) {
                return response.getTip();
            }
        } catch (Exception e) {
            log.error("Python AI 서비스 실제 호출 실패: {}", e.getMessage());
        }

        return createFallbackTip(storeData, weatherData, additionalRequirement);
    }

    private String createFallbackTip(StoreData storeData, WeatherData weatherData, String additionalRequirement) {
        String businessType = storeData.getBusinessType();
        double temperature = weatherData.getTemperature();
        String condition = weatherData.getCondition();
        String storeName = storeData.getStoreName();

        // 추가 요청사항이 있는 경우 우선 반영
        if (additionalRequirement != null && !additionalRequirement.trim().isEmpty()) {
            return String.format("%s에서 %s를 고려한 특별한 서비스로 고객들을 맞이해보세요!",
                    storeName, additionalRequirement);
        }

        // 날씨와 업종 기반 규칙
        if (temperature > 25) {
            if (businessType.contains("카페")) {
                return String.format("더운 날씨(%.1f도)에는 시원한 아이스 음료와 디저트로 고객들을 시원하게 만족시켜보세요!", temperature);
            } else {
                return "더운 여름날, 시원한 음료나 냉면으로 고객들에게 청량감을 선사해보세요!";
            }
        } else if (temperature < 10) {
            if (businessType.contains("카페")) {
                return String.format("추운 날씨(%.1f도)에는 따뜻한 음료와 베이커리로 고객들에게 따뜻함을 전해보세요!", temperature);
            } else {
                return "추운 겨울날, 따뜻한 국물 요리로 고객들의 몸과 마음을 따뜻하게 해보세요!";
            }
        }

        if (condition.contains("비")) {
            return "비 오는 날에는 따뜻한 음료와 분위기로 고객들의 마음을 따뜻하게 해보세요!";
        }

        // 기본 팁
        return String.format("%s에서 오늘(%.1f도, %s) 같은 날씨에 어울리는 특별한 서비스로 고객들을 맞이해보세요!",
                storeName, temperature, condition);
    }

    private static class PythonAiResponse {
        private String tip;
        private String status;
        private String message;

        public String getTip() { return tip; }
        public void setTip(String tip) { this.tip = tip; }
        public String getStatus() { return status; }
        public void setStatus(String status) { this.status = status; }
        public String getMessage() { return message; }
        public void setMessage(String message) { this.message = message; }
    }
}