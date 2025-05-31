# spark_average_speed.py
import sys
from datetime import datetime
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import json
import boto3
from botocore.config import Config

def get_day_of_week(timestamp):
    """
    Converts a Unix timestamp to the day of the week (0=Monday, 6=Sunday).
    """
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.weekday()

if __name__ == "__main__":
    # Configure Spark
    conf = SparkConf().setAppName("AverageSpeedByDayOfWeek").setMaster("spark://spark-master:7077")
    sc = SparkContext(conf=conf)
    spark = SparkSession.builder.config(conf=conf).getOrCreate()

    try:
        s3_client = boto3.client('s3', 
            endpoint_url='http://localstack:4566',
            aws_access_key_id='test',
            aws_secret_access_key='test',
            region_name='us-east-1')
        
        # Read data from S3 using boto3
        response = s3_client.get_object(Bucket='routes-bucket', Key='routes.json')
        content = response['Body'].read().decode('utf-8')
        
        # Parse JSON data
        routes_data = [json.loads(line) for line in content.strip().split('\n') if line.strip()]
        
        # Convert to DataFrame
        df = spark.createDataFrame(routes_data)
        
        # Convert timestamp to day of week and calculate average speed
        from pyspark.sql.functions import udf, avg
        from pyspark.sql.types import IntegerType
        
        # Create UDF for day of week calculation
        day_of_week_udf = udf(get_day_of_week, IntegerType())
        
        # Add day of week column and group by it
        result_df = df.withColumn("day_of_week", day_of_week_udf("timestamp")) \
                     .groupBy("day_of_week") \
                     .agg(avg("speed").alias("average_speed"))
        
        # Collect and print results
        results = result_df.collect()
        
        # Map weekday number to name for better readability
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        print("Average speed by day of the week:")
        for row in sorted(results, key=lambda x: x["day_of_week"]):
            print(f"{day_names[row['day_of_week']]}: {row['average_speed']:.2f} km/h")

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        spark.stop()
        sc.stop()