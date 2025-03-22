from kafka import KafkaProducer
import json
import time
import requests

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Function to fetch weather data
def fetch_weather_data(city):
    api_key = 'fae9eba41841695b89acc18d4307f0dc'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# Send weather data to Kafka topic
def send_weather_data(city):
    while True:
        data = fetch_weather_data(city)
        if data:
            producer.send('weather-data-pro1', data)
            print(f"Sent: {json.dumps(data, indent=2)}")
        time.sleep(20)  # Fetch every 60 seconds

# Start sending weather updates for London
send_weather_data('London')

