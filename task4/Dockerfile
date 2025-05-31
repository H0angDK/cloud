# Dockerfile
FROM ubuntu:22.04 AS downloader

# Install curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Create directory for downloads
WORKDIR /downloads

# Download the JAR files
RUN curl -L https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.6/hadoop-aws-3.3.6.jar -o hadoop-aws-3.3.6.jar \
    && curl -L https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar -o aws-java-sdk-bundle-1.12.262.jar

# Final stage
FROM bitnami/spark:3.5.1

WORKDIR /app

# Install Python packages
RUN pip install boto3

# Copy the downloaded JAR files from the downloader stage
COPY --from=downloader /downloads/hadoop-aws-3.3.6.jar /opt/bitnami/spark/jars/
COPY --from=downloader /downloads/aws-java-sdk-bundle-1.12.262.jar /opt/bitnami/spark/jars/

# Start Spark worker
CMD ["/opt/bitnami/scripts/spark/run.sh"]