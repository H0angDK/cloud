import boto3
import json
import random
import time
from datetime import datetime
import os

# Constants
STREAM_NAME = "vehicle-speed-stream"
NUM_VEHICLES = 5
SPEED_RANGE = (30, 100)  # km/h

def create_kinesis_client():
    return boto3.client(
        'kinesis',
        endpoint_url=os.getenv('AWS_ENDPOINT_URL', 'http://localhost:4566'),
        region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', 'test'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'test')
    )

def create_stream(client):
    try:
        client.create_stream(
            StreamName=STREAM_NAME,
            ShardCount=1
        )
        print(f"Created stream: {STREAM_NAME}")
    except client.exceptions.ResourceInUseException:
        print(f"Stream {STREAM_NAME} already exists")

def generate_speed_data():
    vehicle_id = f"VEH{random.randint(1, NUM_VEHICLES):03d}"
    speed = random.randint(*SPEED_RANGE)
    timestamp = datetime.now().isoformat()
    
    return {
        'vehicle_id': vehicle_id,
        'speed': speed,
        'timestamp': timestamp
    }

def main():
    client = create_kinesis_client()
    create_stream(client)
    
    print("Starting to send test data...")
    try:
        while True:
            data = generate_speed_data()
            response = client.put_record(
                StreamName=STREAM_NAME,
                Data=json.dumps(data),
                PartitionKey=data['vehicle_id']
            )
            print(f"Sent data: {data}")
            time.sleep(1)  # Send one record per second
    except KeyboardInterrupt:
        print("\nStopped sending test data")

if __name__ == '__main__':
    main() 