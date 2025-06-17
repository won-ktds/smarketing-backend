//package com.won.smarketing.recommend.config;
//
//import com.azure.messaging.eventhubs.EventHubClientBuilder;
//import com.azure.messaging.eventhubs.EventHubProducerClient;
//import org.springframework.beans.factory.annotation.Value;
//import org.springframework.context.annotation.Bean;
//import org.springframework.context.annotation.Configuration;
//
//@Configuration
//public class EventHubConfig {
//
//    @Value("${spring.cloud.azure.eventhubs.connection-string}")
//    private String connectionString;
//
//    @Value("${azure.eventhub.marketing-tip-hub}")
//    private String marketingTipHub;
//
//    @Bean
//    public EventHubProducerClient marketingTipProducerClient() {
//        return new EventHubClientBuilder()
//                .connectionString(connectionString, marketingTipHub)
//                .buildProducerClient();
//    }
//}
