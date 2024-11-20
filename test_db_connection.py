import os
import django
from django.db import connections
from django.db.utils import OperationalError

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangify_backed.production')
django.setup()

def test_db_connection():
    db_conn = connections['default']
    try:
        db_conn.cursor()
        print('Database connection successful!')
    except OperationalError as e:
        print('Database connection failed!')
        print(f'Error: {e}')

if __name__ == '__main__':
    test_db_connection()
    print("DATABASE_URL:", os.getenv('DATABASE_URL'))
