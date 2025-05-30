import json
import boto3
from datetime import datetime, timedelta
from collections import defaultdict

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

table = dynamodb.Table('gps_locations')

def calculate_travel_time(locations):
    if len(locations) < 2:
        return 0
    
    # Sort locations by timestamp
    sorted_locations = sorted(locations, key=lambda x: x['timestamp'])
    
    # Calculate total time difference (timestamps are in seconds)
    start_time = sorted_locations[0]['timestamp']
    end_time = sorted_locations[-1]['timestamp']
    
    return (end_time - start_time) / 60  # Convert to minutes

def get_all_items(filter_expression=None, expression_values=None, expression_names=None):
    items = []
    last_evaluated_key = None
    
    while True:
        if last_evaluated_key:
            if filter_expression:
                response = table.scan(
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_values,
                    ExpressionAttributeNames=expression_names,
                    ExclusiveStartKey=last_evaluated_key
                )
            else:
                response = table.scan(ExclusiveStartKey=last_evaluated_key)
        else:
            if filter_expression:
                response = table.scan(
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_values,
                    ExpressionAttributeNames=expression_names
                )
            else:
                response = table.scan()
        
        items.extend(response['Items'])
        
        if 'LastEvaluatedKey' not in response:
            break
            
        last_evaluated_key = response['LastEvaluatedKey']
    
    return items

def lambda_handler(event, context):
    try:
        # Get filter parameters from event
        device_id = event.get('device_id')
        start_time = event.get('start_time')
        end_time = event.get('end_time')
        
        # Build filter expression if parameters are provided
        filter_expression = None
        expression_values = {}
        expression_names = {'#ts': 'timestamp'}
        
        if device_id:
            filter_expression = 'device_id = :device_id'
            expression_values[':device_id'] = device_id
            
        if start_time:
            if filter_expression:
                filter_expression += ' AND #ts >= :start_time'
            else:
                filter_expression = '#ts >= :start_time'
            expression_values[':start_time'] = start_time
            
        if end_time:
            if filter_expression:
                filter_expression += ' AND #ts <= :end_time'
            else:
                filter_expression = '#ts <= :end_time'
            expression_values[':end_time'] = end_time
        
        # Get all items with pagination
        items = get_all_items(filter_expression, expression_values, expression_names)
        
        # Group locations by device_id
        device_locations = defaultdict(list)
        for item in items:
            device_locations[item['device_id']].append(item)
        
        # Calculate analytics for each device
        analytics = {}
        for device_id, locations in device_locations.items():
            # Sort locations by timestamp
            sorted_locations = sorted(locations, key=lambda x: x['timestamp'])
            travel_time = calculate_travel_time(sorted_locations)
            analytics[device_id] = {
                'average_travel_time_minutes': travel_time,
                'total_locations': len(locations),
                'first_location_time': sorted_locations[0]['timestamp'],
                'last_location_time': sorted_locations[-1]['timestamp']
            }
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'analytics': analytics
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 