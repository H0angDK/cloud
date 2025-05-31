import boto3
import os
import zipfile
import shutil

def create_dynamodb_table():
    print("Creating DynamoDB table...")
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url='http://localhost:4566',
        region_name='us-east-1',
        aws_access_key_id='test',
        aws_secret_access_key='test'
    )

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
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("DynamoDB table created successfully!")
    except Exception as e:
        print(f"Error creating DynamoDB table: {str(e)}")

def create_lambda_package(lambda_name):
    print(f"Creating Lambda package for {lambda_name}...")
    zip_filename = f"{lambda_name}.zip"
    
    # Create a temporary directory for the package
    if os.path.exists('temp'):
        shutil.rmtree('temp')
    os.makedirs('temp')
    
    # Copy the Lambda function to temp directory
    shutil.copy(f"lambda/{lambda_name}.py", f"temp/{lambda_name}.py")
    
    # Create zip file
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(f"temp/{lambda_name}.py", f"{lambda_name}.py")
    
    # Clean up temp directory
    shutil.rmtree('temp')
    
    return zip_filename

def create_lambda_function(function_name, zip_filename):
    print(f"Creating Lambda function {function_name}...")
    lambda_client = boto3.client(
        'lambda',
        endpoint_url='http://localhost:4566',
        region_name='us-east-1',
        aws_access_key_id='test',
        aws_secret_access_key='test'
    )

    try:
        with open(zip_filename, 'rb') as f:
            lambda_client.create_function(
                FunctionName=function_name,
                Runtime='python3.8',
                Handler=f"{function_name}.lambda_handler",
                Role='arn:aws:iam::000000000000:role/lambda-role',
                Code={'ZipFile': f.read()}
            )
        print(f"Lambda function {function_name} created successfully!")
    except Exception as e:
        print(f"Error creating Lambda function {function_name}: {str(e)}")

def main():
    # Create DynamoDB table
    create_dynamodb_table()

    # Create Lambda packages and functions
    lambda_functions = ['save_location', 'get_analytics']
    
    for func_name in lambda_functions:
        zip_file = create_lambda_package(func_name)
        create_lambda_function(func_name, zip_file)
        # Clean up zip file
        os.remove(zip_file)

    print("Setup completed!")

if __name__ == "__main__":
    main() 