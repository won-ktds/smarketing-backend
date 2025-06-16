# Multi-stage build for Spring Boot application
FROM gradle:8.13-jdk17 AS builder

# Build arguments
ARG BUILD_LIB_DIR
ARG ARTIFACTORY_FILE

WORKDIR /app

# Copy source code (assumed to be already built)
# The JAR file should be copied from the build context
COPY ${BUILD_LIB_DIR}/${ARTIFACTORY_FILE} app.jar

# Runtime stage
FROM eclipse-temurin:17-jre

# Install necessary packages
RUN apt-get update && apt-get install -y \
    curl \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /app/app.jar app.jar

# Change ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port (will be overridden by environment variables)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/actuator/health || exit 1

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]
