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

    min_salary = 70000

    # Parameterized query (%s placeholder prevents SQL injection)
    query = 'SELECT job_title, salary_min, salary_max FROM jobs WHERE salary_min >= %s'
    cursor.execute(query, (min_salary,))  # Pass tuple (min_salary,)

    jobs = cursor.fetchall()

    print(f'=== Jobs with salary >= ${min_salary:,} ===')
    print(f'Found {len(jobs)} jobs')
    print()

    for job in jobs:
        title, sal_min, sal_max = job
        print(f'{title}: ${sal_min:,.0f} - ${sal_max:,.0f}')

except mysql.connector.Error as error:
    print(f'Error: {error}')

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
