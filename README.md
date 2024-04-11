## Disclaimer: This is for lab 10, and the final Project

### For lab 8,9 and 10, use the GCP, it's way easier

Open the `download.py` file and configure the number of records you want to use for your project

```
total_records_to_fetch = 500000  # Total number of records you want to fetch
```

Run the file `python download.py`

Move the downloaded file to > `/logstash/nyc_311_service_requests_data.json`

Download the cars.csv file and move it to  > `/logstash_lab10/cars.csv`

Make sure the name of the file is `cars.csv`

For the final project, write your config file and name it `logstash-finalproject.conf`

Move it to `/logstash/logstash-finalproject.conf`

I wrote the geopoint file for you so you're all good


1. Download docker and make sure it's running
2. Ensure you have docker compose as well
3. run `docker-compose up -d`
4. Everything should be working so you can run everything locally

 
The services should look like this:
You can click on it to show the app in your local setup

<img width="1421" alt="Screenshot 2024-04-08 at 11 18 59" src="https://github.com/Justicea83/elkstack/assets/26106822/01f9e9d2-0f89-43f4-af15-8d5c9d27b072">

If you don't have enough memory on your PC, copy the codes onto the GCP and follow the instructions
