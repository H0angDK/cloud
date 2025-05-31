import boto3
import json
from botocore.config import Config
endpoint_url = "http://localstack:4566"

# Create S3 client
def setup_s3():

    s3 = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id='test',
        aws_secret_access_key='test',
        region_name='us-east-1'
    )
    
    # Create bucket
    bucket_name = 'routes-bucket'
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"Created bucket: {bucket_name}")
    except Exception as e:
        print(f"Bucket might already exist: {e}")

    # Sample data
    sample_data = [
        {"timestamp": 1709251200, "speed": 65.5},
        {"timestamp": 1709337600, "speed": 70.2},
        {"timestamp": 1709424000, "speed": 68.9},
        {"timestamp": 1709510400, "speed": 72.1},
        {"timestamp": 1709596800, "speed": 69.8},
        {"timestamp": 1709683200, "speed": 75.3},
        {"timestamp": 1709769600, "speed": 71.2},
        {"timestamp": 1709856000, "speed": 67.8},
        {"timestamp": 1709942400, "speed": 73.4},
        {"timestamp": 1710028800, "speed": 69.1}
    ]

    # Convert to JSON lines format
    json_data = '\n'.join([json.dumps(record) for record in sample_data])

    # Upload data to S3
    try:
        s3.put_object(
            Bucket=bucket_name,
            Key='routes.json',
            Body=json_data
        )
        print("Successfully uploaded sample data to S3")
    except Exception as e:
        print(f"Error uploading data: {e}")

if __name__ == "__main__":
    setup_s3() 