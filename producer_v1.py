import requests
from kafka import KafkaProducer
import json
import time

##kafka setup
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

## weather API setup
API_KEY = 'fae9eba41841695b89acc18d4307f0dc'
CITY = 'london'
url = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}'

def fetch_weather_data():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            'city': CITY,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'timestamp': int(time.time())
        }
        return weather_info
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

while True:
    weather_data = fetch_weather_data()
    if weather_data:
        producer.send('weather_data', value= weather_data)
        print(f"Sent: {weather_data}")
    time.sleep(60) ## fetch every minute