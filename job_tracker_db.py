import mysql.connector
from mysql.connector import Error


class JobTrackerDB:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'root123;',  # Your MySQL password
            'database': 'job_tracker'
        }
        self.connection = None

    def connect(self):
        """Establishes connection to the MySQL database."""
        try:
            self.connection = mysql.connector.connect(**self.config)
            return True
        except Error as e:
            print(f'Connection error: {e}')
            return False

    def disconnect(self):
        """Closes the active database connection if open."""
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def get_all_companies(self):
        """Fetches all companies as dictionaries."""
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM companies')
        results = cursor.fetchall()
        cursor.close()
        return results

    def get_jobs_by_salary(self, min_salary):
        """Fetches jobs meeting or exceeding minimum salary using parameterized query."""
        cursor = self.connection.cursor(dictionary=True)
        query = 'SELECT * FROM jobs WHERE salary_min >= %s'
        cursor.execute(query, (min_salary,))
        results = cursor.fetchall()
        cursor.close()
        return results

    def add_application(self, job_id, status='Applied'):
        """Inserts a new job application and returns the generated application ID."""
        cursor = self.connection.cursor()
        query = '''
        INSERT INTO applications (job_id, application_date, status)
        VALUES (%s, CURDATE(), %s)
        '''
        cursor.execute(query, (job_id, status))
        self.connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return new_id


# Example usage / Test Block
if __name__ == '__main__':
    db = JobTrackerDB()
    if db.connect():
        print("=== Testing JobTrackerDB Module ===")
        companies = db.get_all_companies()
        print(f'Found {len(companies)} companies:')
        for c in companies:
            print(f" - {c['company_name']}")

        db.disconnect()
        print("Database connection closed.")
