from dotenv import load_dotenv
import os
from kafka import KafkaConsumer
import snowflake.connector
import json
from datetime import datetime

def consume_and_insert_weather_data():
    ##kafka setup
    consumer = KafkaConsumer(
        'weather_data',
        bootstrap_servers = 'localhost:9092',
        value_deserializer = lambda v : json.loads(v)
    )

    # Load environment variables from .env file
    load_dotenv()

    ### snowflake setup
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE"),
        authenticator='snowflake'
    )

    cursor = conn.cursor()

    ## create table in snowflake
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS WEATHER_DATA(
            city STRING,
            temperature FLOAT,
            humidity FLOAT,
            timestamp TIMESTAMP
        )"""
    )

    cursor.execute("ALTER SESSION SET TIMESTAMP_INPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS'")


    for message in consumer:
        weather_data = message.value
        timestamp = datetime.fromtimestamp(weather_data['timestamp'])
        cursor.execute("""
                INSERT INTO WEATHER_DATA (city, temperature, humidity, timestamp)
                VALUES (%s, %s, %s, %s)
            """, (
            weather_data['city'],
            weather_data['temperature'],
            weather_data['humidity'],
            # weather_data['timestamp']
            timestamp
        ))
        print(f"inserted weather data : {weather_data}")