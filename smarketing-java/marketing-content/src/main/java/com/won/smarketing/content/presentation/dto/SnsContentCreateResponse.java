package com.won.smarketing.content.presentation.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

/**
 * SNS 콘텐츠 생성 응답 DTO
 *
 * AI를 통해 SNS 콘텐츠를 생성한 후 클라이언트에게 반환되는 응답 정보입니다.
 * 생성된 콘텐츠의 기본 정보와 함께 사용자가 추가 편집할 수 있는 정보를 포함합니다.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "SNS 콘텐츠 생성 응답")
@JsonIgnoreProperties(ignoreUnknown = true)
public class SnsContentCreateResponse {
    @Schema(description = "생성된 콘텐츠")
    private String content;
}