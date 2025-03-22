from kafka import KafkaConsumer
import json

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    'weather-data-pro1',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Process and display weather updates
for message in consumer:
    weather_data = message.value
    city = weather_data['main']
    temp = round(weather_data['main']['temp'] - 273.15, 2)  # Convert Kelvin to Celsius
    condition = weather_data['weather'][0]['description']

    print(f"City: {city}, Temperature: {temp}°C, Condition: {condition}")