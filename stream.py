import requests
import json
import time
from confluent_kafka import Producer


def fetch_data(url, retries=3, backoff_factor=0.5):
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            if attempt == retries:
                print(f"Final attempt failed with error: {e}")
                return None
            else:
                sleep_time = backoff_factor * (2 ** (attempt - 1))
                print(f"Attempt {attempt} failed, retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)


def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed:', err)
    else:
        print('Message delivered to', msg.topic(), msg.partition())


def handle():
    conf = {'bootstrap.servers': 'kafka:9092'}  # Adjust for your Kafka server config
    producer = Producer(**conf)

    offset = 0
    limit = 10  # Adjust the limit as needed
    base_url = "https://nycopendata.socrata.com/resource/erm2-nwe9.json"
    topic = 'nyc_311_service_requests'

    # Loop indefinitely to keep fetching new data
    while True:
        url = f"{base_url}?$limit={limit}&$offset={offset}"
        response = fetch_data(url)

        if response is None:
            break

        data = response.json()

        if not data:
            print("No new data available, waiting before checking again...")
            time.sleep(300)  # Wait for 5 minutes before checking again
            continue  # Skip the rest of the loop and check for new data again

        print(f"Fetched {len(data)} records, offset: {offset}")

        for record in data:
            producer.produce(topic, json.dumps(record).encode('utf-8'), callback=delivery_report)
            producer.poll(0)

        producer.flush()

        offset += limit  # Prepare for the next batch
        print('...Sleeping briefly to avoid rate limiting \n\n')
        time.sleep(2)  # Short sleep to mitigate potential rate limiting

    print("Data publishing to Kafka topic is complete.")


if __name__ == '__main__':
    handle()
