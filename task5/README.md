# Real-time Speed Violation Detection System

This system uses Apache Flink and Amazon Kinesis (simulated with LocalStack) to detect vehicle speed violations in real-time.

## Components

- LocalStack: Simulates AWS Kinesis service locally
- Apache Flink: Processes the streaming data
- Python application: Implements the speed violation detection logic
- Test data generator: Simulates vehicle speed data

## Prerequisites

- Docker
- Docker Compose

## Setup and Running

1. Start the services:
```bash
docker-compose up -d
```

2. Wait for all services to start (about 30 seconds)

3. Generate test data:
```bash
docker-compose exec speed-processor python generate_test_data.py
```

docker-compose exec speed-processor flink run -py speed_processor.py

4. Monitor the Flink job:
- Open http://localhost:8081 in your browser
- Navigate to the "Jobs" section to see the running job

## How it Works

1. The test data generator creates random vehicle speed data and sends it to Kinesis
2. Flink reads the data from Kinesis
3. The speed processor checks if the speed exceeds the limit (60 km/h)
4. Violations are written to a separate Kinesis stream

## Configuration

- Speed limit: 60 km/h (can be modified in `speed_processor.py`)
- Number of test vehicles: 5 (can be modified in `generate_test_data.py`)
- Speed range: 30-100 km/h (can be modified in `generate_test_data.py`)
speed_processor.py
## Stopping the System

```bash
docker-compose down
``` 