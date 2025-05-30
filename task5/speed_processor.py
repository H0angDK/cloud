import os
import json
import sys
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors.kinesis import KinesisStreamsSink
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.common.time import Time
from pyflink.common.typeinfo import Types
from pyflink.datastream.connectors.kinesis import FlinkKinesisConsumer
from pyflink.datastream.functions import MapFunction
from pyflink.datastream.connectors.kinesis import PartitionKeyGenerator

# Constants
SPEED_LIMIT = 60  # km/h
INPUT_STREAM = "vehicle-speed-stream"
OUTPUT_STREAM = "speed-violations-stream"

# Configure Flink environment
os.environ['PYFLINK_PYTHON'] = '/usr/bin/python3'
os.environ['PYTHONPATH'] = ':'.join(sys.path)

class SpeedViolationProcessor(MapFunction):
    """
    A MapFunction to process incoming vehicle speed data.
    It identifies speed violations based on a predefined SPEED_LIMIT.
    """
    def map(self, value):
        try:
            data = json.loads(value)
            # Check if speed exceeds the limit
            if data['speed'] > SPEED_LIMIT:
                # Return a JSON string indicating a violation
                return json.dumps({
                    'vehicle_id': data['vehicle_id'],
                    'speed': data['speed'],
                    'speed_limit': SPEED_LIMIT,
                    'timestamp': data['timestamp'],
                    'violation': True
                })
        except Exception as e:
            # Catch specific exceptions for better error reporting
            # This helps in debugging issues with malformed input data
            print(f"Error processing record: {value}. Error: {e}")
            # Do not re-raise in production, but for debugging, you might want to.
            # For now, we return None to filter out problematic records.
        return None

def create_kinesis_source():
    """
    Configures and returns a FlinkKinesisConsumer for the input stream.
    """
    kinesis_props = {
        'aws.region': os.getenv('AWS_DEFAULT_REGION', 'us-east-1'),
        'aws.credentials.provider': 'AUTO', # Use automatic credential provider
        'flink.stream.initpos': 'LATEST', # Start reading from the latest records
        # Explicitly set the Kinesis endpoint for LocalStack compatibility
        'aws.endpoint': os.getenv('AWS_ENDPOINT_URL', 'http://localstack:4566')
    }

    return FlinkKinesisConsumer(
        INPUT_STREAM,
        SimpleStringSchema(), # Data is expected to be simple strings
        kinesis_props
    )

def create_kinesis_sink():
    """
    Configures and returns a KinesisStreamsSink for the output stream.
    """
    kinesis_props = {
        'aws.region': os.getenv('AWS_DEFAULT_REGION', 'us-east-1'),
        'aws.credentials.provider': 'AUTO', # Use automatic credential provider
        # Explicitly set the Kinesis endpoint for LocalStack compatibility
        'aws.endpoint': os.getenv('AWS_ENDPOINT_URL', 'http://localstack:4566')
    }

    return KinesisStreamsSink.builder() \
        .set_kinesis_client_properties(kinesis_props) \
        .set_stream_name(OUTPUT_STREAM) \
        .set_serialization_schema(SimpleStringSchema()) \
        .set_partition_key_generator(PartitionKeyGenerator.random()) \
        .build()

def main():
    """
    Main function to set up and execute the Flink streaming job.
    """
    # Set up the execution environment with remote configuration
    env = StreamExecutionEnvironment.get_execution_environment()
    # Checkpointing is crucial for fault tolerance
    env.enable_checkpointing(1000) # Enable checkpointing every 1000 ms

    # Set parallelism for the job. For local testing, 1 is often sufficient.
    env.set_parallelism(1)

    # Create the Kinesis source
    source = create_kinesis_source()
    print(source)   

    print("Creating processing pipeline...")
    # Build the streaming pipeline:
    # 1. Add the Kinesis source
    # 2. Map records using SpeedViolationProcessor to identify violations
    # 3. Filter out None values (records that were not violations or had parsing errors)
    stream = env.add_source(source) \
        .map(SpeedViolationProcessor(), output_type=Types.STRING()) \
        .filter(lambda x: x is not None)

    # Create the Kinesis sink
    sink = create_kinesis_sink()

    # Connect the processed stream to the sink
    stream.sink_to(sink)

    # Execute the Flink job with a descriptive name
    print("Executing Flink job: Speed Violation Detection")
    env.execute("Speed Violation Detection")
    print("Job completed successfully")

if __name__ == '__main__':
    main()
