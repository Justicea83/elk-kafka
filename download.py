import requests
import json
import time


def fetch_data(url, retries=3, backoff_factor=0.5):
    """Attempt to fetch data with retries and exponential backoff."""
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            return response
        except requests.RequestException as e:
            if attempt == retries:
                print(f"Final attempt failed with error: {e}")
                return None  # Return None to indicate failure
            else:
                sleep_time = backoff_factor * (2 ** (attempt - 1))
                print(f"Attempt {attempt} failed, retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)


offset = 0
limit = 50000  # Number of records to fetch per request
total_records_to_fetch = 500000  # Total number of records you want to fetch
records_fetched = 0  # Keep track of the number of records fetched
base_url = "https://nycopendata.socrata.com/resource/erm2-nwe9.json"
file_path = 'nyc_311_service_requests_data.json'

# Open the file in write mode to start fresh
with open(file_path, 'w') as file:
    pass  # Just to clear the file in case it exists

first_batch = True

while records_fetched < total_records_to_fetch:
    actual_limit = min(limit, total_records_to_fetch - records_fetched)  # Adjust limit for the last request
    url = f"{base_url}?$limit={actual_limit}&$offset={offset}"
    response = fetch_data(url)

    if response is None:  # Check if the fetch was unsuccessful
        break

    data = response.json()

    if not data:
        break

    print(f"Fetched {len(data)} records, offset: {offset}")

    # Open the file in append mode
    with open(file_path, 'a') as file:
        for record in data:
            # Write each record as a separate line
            if first_batch:
                first_batch = False
            else:
                file.write('\n')  # New line for each record after the first
            json.dump(record, file)

    records_fetched += len(data)
    offset += actual_limit
    time.sleep(5)  # Sleep to avoid hitting rate limits
    print('...Sleeping to avoid rate limiting \n\n')

print(f"Data has been downloaded and appended to {file_path}")
