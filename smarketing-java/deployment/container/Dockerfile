# Build stage
FROM eclipse-temurin:17-jre AS builder
ARG BUILD_LIB_DIR
ARG ARTIFACTORY_FILE
WORKDIR /app
COPY ${BUILD_LIB_DIR}/${ARTIFACTORY_FILE} app.jar

# Run stage
FROM eclipse-temurin:17-jre

# Install necessary packages
RUN apt-get update && apt-get install -y \
    curl \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

ENV USERNAME k8s
ENV ARTIFACTORY_HOME /home/${USERNAME}
ENV JAVA_OPTS=""

# Add a non-root user
RUN groupadd -r ${USERNAME} && useradd -r -g ${USERNAME} ${USERNAME} && \
    mkdir -p ${ARTIFACTORY_HOME} && \
    chown ${USERNAME}:${USERNAME} ${ARTIFACTORY_HOME}

WORKDIR ${ARTIFACTORY_HOME}

# Copy JAR from builder stage
COPY --from=builder /app/app.jar app.jar
RUN chown ${USERNAME}:${USERNAME} app.jar

# Switch to non-root user
USER ${USERNAME}

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/actuator/health || exit 1

# Run the application
ENTRYPOINT ["sh", "-c"]
CMD ["java ${JAVA_OPTS} -jar app.jar"]
