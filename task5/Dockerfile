FROM flink:1.18.1-scala_2.12

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip wget && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    pip3 install apache-flink==1.18.1 boto3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Copy application code
COPY speed_processor.py /opt/flink/speed_processor.py
COPY generate_test_data.py /opt/flink/generate_test_data.py

# Download correct Kinesis connector
RUN wget https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kinesis/4.3.0-1.18/flink-connector-kinesis-4.3.0-1.18.jar -P /opt/flink/lib

# Set working directory
WORKDIR /opt/flink

# Command to run the application
CMD ["python3", "speed_processor.py"]