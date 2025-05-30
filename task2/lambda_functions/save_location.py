import json
import boto3
from datetime import datetime

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

table = dynamodb.Table('gps_locations')

def lambda_handler(event, context):
    try:
        # Parse the incoming event
        location_data = json.loads(event['body']) if isinstance(event, dict) and 'body' in event else event
        
        # Prepare item for DynamoDB
        item = {
            'device_id': location_data['device_id'],
            'timestamp': location_data['timestamp'],  # Already an integer
            'latitude': location_data['latitude'],
            'longitude': location_data['longitude']
        }
        
        # Save to DynamoDB
        table.put_item(Item=item)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Location saved successfully',
                'data': item
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 