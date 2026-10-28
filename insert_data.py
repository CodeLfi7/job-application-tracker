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

    # New company data
    new_company = {
        'name': 'Python Solutions LLC',
        'industry': 'Software Development',
        'website': 'www.pythonsolutions.com',
        'city': 'Miami',
        'state': 'Florida'
    }

    # Insert query with parameterized values
    insert_query = '''
    INSERT INTO companies (company_name, industry, website, city, state)
    VALUES (%s, %s, %s, %s, %s)
    '''

    values = (
        new_company['name'],
        new_company['industry'],
        new_company['website'],
        new_company['city'],
        new_company['state']
    )

    cursor.execute(insert_query, values)

    # IMPORTANT: Commit the transaction!
    connection.commit()

    print('Company added successfully!')
    print(f'New company ID: {cursor.lastrowid}')

except mysql.connector.Error as error:
    print(f'Error: {error}')
    connection.rollback()  # Undo changes if error

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
