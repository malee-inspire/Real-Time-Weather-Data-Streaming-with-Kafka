# Use the official Airflow image as the base
FROM apache/airflow:2.10.5

# Install psycopg2 (PostgreSQL driver)
RUN pip install --no-cache-dir psycopg2-binary kafka-python