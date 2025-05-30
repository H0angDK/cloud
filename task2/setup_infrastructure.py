import boto3
import json
import os
import zipfile
import shutil

# Initialize boto3 clients for localstack
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

lambda_client = boto3.client(
    'lambda',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

def create_dynamodb_table():
    try:
        table = dynamodb.create_table(
            TableName='gps_locations',
            KeySchema=[
                {
                    'AttributeName': 'device_id',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'timestamp',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'device_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'timestamp',
                    'AttributeType': 'N'  # Changed to Number type for integer timestamps
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("DynamoDB table created successfully!")
        return table
    except Exception as e:
        print(f"Error creating DynamoDB table: {str(e)}")
        return None

def create_lambda_function(function_name, handler_file):
    try:
        # Create a temporary directory for the Lambda package
        temp_dir = f"temp_{function_name}"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Copy the handler file to the temporary directory
        shutil.copy(handler_file, os.path.join(temp_dir, "lambda_function.py"))
        
        # Create a ZIP file
        zip_path = f"{function_name}.zip"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(os.path.join(temp_dir, "lambda_function.py"), "lambda_function.py")
        
        # Read the ZIP file
        with open(zip_path, 'rb') as f:
            zip_bytes = f.read()
        
        # Create the Lambda function
        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python3.9',
            Role='arn:aws:iam::000000000000:role/lambda-role',
            Handler='lambda_function.lambda_handler',
            Code={
                'ZipFile': zip_bytes
            }
        )
        
        print(f"Lambda function {function_name} created successfully!")
        
        # Clean up
        shutil.rmtree(temp_dir)
        os.remove(zip_path)
        
        return response
    except Exception as e:
        print(f"Error creating Lambda function {function_name}: {str(e)}")
        return None

def main():
    # Create DynamoDB table
    create_dynamodb_table()
    
    # Create Lambda functions
    create_lambda_function('save-location', 'lambda_functions/save_location.py')
    create_lambda_function('get-analytics', 'lambda_functions/get_analytics.py')

if __name__ == "__main__":
    main() 