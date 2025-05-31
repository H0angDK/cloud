import json
import boto3
import time

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

table = dynamodb.Table('gps_locations')

def calculate_average_travel_time(device_data):
    if len(device_data) < 2:
        return 0
    
    # Sort by timestamp
    sorted_data = sorted(device_data, key=lambda x: x['timestamp'])
    
    # Calculate time differences
    total_time = 0
    for i in range(1, len(sorted_data)):
        current_time = sorted_data[i]['timestamp']
        previous_time = sorted_data[i-1]['timestamp']
        time_diff = current_time - previous_time
        total_time += time_diff
    
    return total_time / (len(sorted_data) - 1)

def lambda_handler(event, context):
    try:
        # Get all items from DynamoDB
        response = table.scan()
        items = response.get('Items', [])
        
        # Group data by device_id
        device_data = {}
        for item in items:
            device_id = item['device_id']
            if device_id not in device_data:
                device_data[device_id] = []
            device_data[device_id].append(item)
        
        # Calculate analytics for each device
        analytics = {}
        for device_id, data in device_data.items():
            analytics[device_id] = {
                'average_travel_time_seconds': calculate_average_travel_time(data),
                'total_locations': len(data),
                'first_location': min(data, key=lambda x: x['timestamp']),
                'last_location': max(data, key=lambda x: x['timestamp'])
            }
        
        return {
            'statusCode': 200,
            'body': analytics
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 