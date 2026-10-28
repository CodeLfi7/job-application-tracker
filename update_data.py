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

    # Update application status
    application_id = 1
    new_status = 'Offer Accepted'

    update_query = '''
    UPDATE applications
    SET status = %s
    WHERE application_id = %s
    '''

    cursor.execute(update_query, (new_status, application_id))
    connection.commit()

    # Check how many rows were affected
    if cursor.rowcount > 0:
        print(f'Updated {cursor.rowcount} application(s)')
        print(f'Application {application_id} status changed to: {new_status}')
    else:
        print('No applications were updated. Check the ID.')

except mysql.connector.Error as error:
    print(f'Error: {error}')
    connection.rollback()

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
