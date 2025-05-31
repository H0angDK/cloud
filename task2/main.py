from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import json
from typing import Optional
import time

app = FastAPI(
    title="GPS Tracker API",
    description="API for tracking GPS coordinates and analytics",
    version="1.0.0"
)

# Initialize boto3 client for Lambda
lambda_client = boto3.client(
    'lambda',
    endpoint_url='http://localhost:4566',  # LocalStack endpoint
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

class LocationData(BaseModel):
    latitude: float
    longitude: float
    device_id: str
    timestamp: Optional[int] = None

@app.post("/location")
async def save_location(location: LocationData):
    try:
        # Prepare payload for Lambda
        payload = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "device_id": location.device_id,
            "timestamp": location.timestamp if location.timestamp else int(time.time())
        }
        
        # Invoke save-location Lambda
        response = lambda_client.invoke(
            FunctionName='save-location',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        
        response_payload = json.loads(response['Payload'].read())
        
        if response_payload.get('statusCode') != 200:
            raise HTTPException(status_code=500, detail="Failed to save location")
            
        return {"message": "Location saved successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics")
async def get_analytics():
    try:
        # Invoke get-analytics Lambda
        response = lambda_client.invoke(
            FunctionName='get-analytics',
            InvocationType='RequestResponse'
        )
        
        response_payload = json.loads(response['Payload'].read())
        
        if response_payload.get('statusCode') != 200:
            raise HTTPException(status_code=500, detail="Failed to get analytics")
            
        return response_payload.get('body', {})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 