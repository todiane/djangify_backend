from decouple import Config, RepositoryEnv
import psycopg2

# Load the production environment file
config = Config(RepositoryEnv('.env.production'))

# Get the production DATABASE_URL
DATABASE_URL = config('DATABASE_URL')

# Initialize the connection variable
connection = None

try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    # Execute a simple query
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()

    print(f"Connected to the database. PostgreSQL version: {db_version}")

except Exception as error:
    print(f"Error connecting to the database: {error}")

finally:
    # Close the connection
    if connection:
        cursor.close()
        connection.close()
        print("Database connection closed.")
