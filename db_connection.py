import mysql.connector

# Database connection configuration
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123;',  # Replace with your MySQL root password
    'database': 'job_tracker'
}

# Try to connect
try:
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        print('Successfully connected to MySQL!')
        print(f'Server version: {connection.get_server_info()}')

        # Get database info
        cursor = connection.cursor()
        cursor.execute('SELECT DATABASE();')
        database_name = cursor.fetchone()[0]
        print(f'Connected to database: {database_name}')

except mysql.connector.Error as error:
    print(f'Error connecting to MySQL: {error}')

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print('Connection closed.')
