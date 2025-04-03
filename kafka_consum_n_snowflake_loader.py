from kafka import KafkaConsumer
import snowflake.connector
import json
import time


##kafka setup
consumer = KafkaConsumer(
    'weather_data',
    bootstrap_servers = 'localhost:9092',
    value_deserializer = lambda v : json.loads(v)
)

### snowflake setup
conn = snowflake.connector.connect(
    user = 'LOARAZEN',
    password = 'Snowflake4loarazen',
    account = 'XNB67701',
    warehouse = 'COMPUTE_WH',
    database = 'KAFKA_SAMPLE_DATA',
    schema = 'KAFKA_SCHEMA'
)

cursor = conn.cursor()

## create table in snowflake
cursor.execute(
    """ CREATE TABLE IF NOT EXISTS WEATHER_DATA(
        city string,
        temperature float,
        humidity float,
        timestamp timestamp
    )"""
)

for message in consumer:
    weather_data = message.value
    cursor.execute(
        """
        INSERT INTO WEATHER_DATA(city, temperature, humidity, timestamp)
        VALUES (%, %, %, %) """ ,
(weather_data['city'],
        weather_data['temperature'],
        weather_data['humidity'],
        weather_data['timestamp']
        ))
    print(f"inserted weather data : {weather_data}")