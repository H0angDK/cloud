from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import json
from typing import Optional
from datetime import datetime

app = FastAPI(
    title="GPS Tracker API",
    description="API for tracking GPS coordinates and analyzing travel time",
    version="1.0.0"
)

class Location(BaseModel):
    latitude: float
    longitude: float
    device_id: str
    timestamp: Optional[int] = None

# Initialize boto3 client for localstack
lambda_client = boto3.client(
    'lambda',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

@app.post("/location")
async def save_location(location: Location):
    try:
        # Prepare payload for Lambda
        payload = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "device_id": location.device_id,
            "timestamp": location.timestamp if location.timestamp else int(datetime.now().timestamp())
        }
        
        # Invoke save-location Lambda
        response = lambda_client.invoke(
            FunctionName='save-location',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        
        return {"message": "Location saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics")
async def get_analytics(device_id: Optional[str] = None, start_time: Optional[int] = None, end_time: Optional[int] = None):
    try:
        # Prepare payload for Lambda
        payload = {
            "device_id": device_id,
            "start_time": start_time,
            "end_time": end_time
        }
        
        # Invoke get-analytics Lambda
        response = lambda_client.invoke(
            FunctionName='get-analytics',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        
        # Parse Lambda response
        response_payload = json.loads(response['Payload'].read())
        return response_payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 