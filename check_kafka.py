import time
from kafka import KafkaConsumer
from subprocess import call

# Kafka configuration
kafka_broker = 'kafka:9092'
kafka_topic = 'nyc_311_service_requests'  # Specify your topic
timeout = 30  # Time to wait for Kafka to become available, in seconds


def check_kafka_connection(broker):
    """Attempt to connect to the specified Kafka broker."""
    try:
        # Attempt to create a Kafka consumer and subscribe to the topic
        consumer = KafkaConsumer(
            bootstrap_servers=[broker],
            consumer_timeout_ms=1000,  # Wait for 1 second
            api_version=(0, 10),  # Adjust this as necessary
        )
        consumer.close()
        print("Kafka is available!")
        return True
    except Exception as e:
        print(f"Waiting for Kafka at {broker}... Error: {e}")
        return False


def execute_script():
    """Execute the download script once Kafka is available."""
    # Replace 'download.py' with the path to your script if it's different
    call(["python", "/app/stream.py"])


if __name__ == '__main__':
    start_time = time.time()
    while True:
        if check_kafka_connection(kafka_broker):
            execute_script()
            break
        if time.time() - start_time > timeout:
            print("Kafka is not available, exiting.")
            break
        time.sleep(5)  # Wait for 5 seconds before trying again
