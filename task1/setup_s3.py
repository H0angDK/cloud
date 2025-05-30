import boto3
import os
import json

# LocalStack endpoint
endpoint_url = "http://localhost:4566"

# Create S3 client
s3 = boto3.client(
    's3',
    endpoint_url=endpoint_url,
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

# Bucket name
bucket_name = 'transport-dashboard'

def create_bucket():
    try:
        # Create bucket
        s3.create_bucket(Bucket=bucket_name)
        print(f"Created bucket: {bucket_name}")
        
        # Configure bucket for static website hosting
        s3.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration={
                'IndexDocument': {'Suffix': 'index.html'},
                'ErrorDocument': {'Key': 'index.html'}
            }
        )
        print("Configured bucket for static website hosting")
        
        # Set bucket policy to allow public access
        bucket_policy = {
            'Version': '2012-10-17',
            'Statement': [{
                'Sid': 'PublicReadGetObject',
                'Effect': 'Allow',
                'Principal': '*',
                'Action': 's3:GetObject',
                'Resource': f'arn:aws:s3:::{bucket_name}/*'
            }]
        }
        s3.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(bucket_policy)
        )
        print("Set bucket policy for public access")
        
    except Exception as e:
        print(f"Error creating bucket: {e}")

def upload_files():
    # Files to upload
    files = ['index.html', 'styles.css', 'map.js', 'chart.js']
    
    for file in files:
        try:
            s3.upload_file(
                file,
                bucket_name,
                file,
                ExtraArgs={'ContentType': 'text/html' if file.endswith('.html') else 
                          'text/css' if file.endswith('.css') else 
                          'application/javascript'}
            )
            print(f"Uploaded {file}")
        except Exception as e:
            print(f"Error uploading {file}: {e}")

if __name__ == "__main__":
    create_bucket()
    upload_files()
    print("\nSetup complete! You can access the website at:")
    print(f"http://localhost:4566/{bucket_name}/index.html") 