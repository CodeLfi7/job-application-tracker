import mysql.connector

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123;',
    'database': 'job_tracker'
}

try:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Delete the company we added in Part 4
    company_name = 'Python Solutions LLC'

    # Safely inspect what will be deleted first
    cursor.execute('SELECT * FROM companies WHERE company_name = %s', (company_name,))
    to_delete = cursor.fetchall()

    if to_delete:
        print(f'About to delete: {to_delete}')

        # Perform delete using parameterized query
        delete_query = 'DELETE FROM companies WHERE company_name = %s'
        cursor.execute(delete_query, (company_name,))
        connection.commit()

        print(f'Deleted {cursor.rowcount} company(ies)')
    else:
        print('Company not found.')

except mysql.connector.Error as error:
    print(f'Error: {error}')
    connection.rollback()

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
