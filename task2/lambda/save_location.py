import json
import boto3
import os
import time

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
        body = json.loads(event) if isinstance(event, str) else event
        
        # Extract location data
        location_data = {
            'device_id': body['device_id'],
            'timestamp': body['timestamp'],
            'latitude': body['latitude'],
            'longitude': body['longitude']
        }
        
        # Save to DynamoDB
        table.put_item(Item=location_data)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Location saved successfully',
                'data': location_data
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 