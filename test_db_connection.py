import os
import sys
import psycopg2
import time
from urllib.parse import urlparse

def test_db_connection():
    url = os.getenv('DATABASE_URL')
    if not url:
        print("No DATABASE_URL environment variable found")
        sys.exit(1)

    # Parse the DATABASE_URL to get components
    parsed = urlparse(url)
    dbname = parsed.path[1:]  # Remove leading slash
    user = parsed.username
    password = parsed.password
    host = parsed.hostname
    port = parsed.port

    # Construct connection string with individual components
    conn_params = {
        'dbname': dbname,
        'user': user,
        'password': password,
        'host': host,
        'port': port
    }

    max_retries = 5
    retry_delay = 5

    for attempt in range(max_retries):
        try:
            print(f"Attempting to connect to PostgreSQL (Attempt {attempt + 1}/{max_retries})")
            print(f"Host: {host}, Port: {port}, Database: {dbname}, User: {user}")
            
            conn = psycopg2.connect(**conn_params)
            conn.close()
            print("Successfully connected to the database")
            return True
        except psycopg2.OperationalError as e:
            print(f"Connection error: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Failed to connect after {max_retries} attempts")
                sys.exit(1)

if __name__ == '__main__':
    test_db_connection()
    