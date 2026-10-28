from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database configuration dictionary (matching your db_connection.py)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123;',
    'database': 'job_tracker'
}


def get_db_connection():
    """Helper function to open a new database connection."""
    conn = mysql.connector.connect(**db_config)
    return conn


@app.route('/')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get total count of applications for the dashboard stats
    cursor.execute('SELECT COUNT(*) as count FROM applications')
    stats = cursor.fetchone()

    cursor.close()
    conn.close()
    return render_template('dashboard.html', stats=stats)

@app.route('/companies')
def companies():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM companies')
    companies_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('companies.html', companies=companies_list)


@app.route('/add_company', methods=['POST'])
def add_company():
    company_name = request.form['company_name']
    industry = request.form['industry']
    website = request.form['website']
    city = request.form['city']
    state = request.form['state']
    notes = request.form['notes']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO companies (company_name, industry, website, city, state, notes)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (company_name, industry, website, city, state, notes))

    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/companies')


@app.route('/delete_company/<int:company_id>', methods=['POST'])
def delete_company(company_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM companies WHERE company_id = %s', (company_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('companies'))


@app.route('/edit_company/<int:company_id>', methods=['GET', 'POST'])
def edit_company(company_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        company_name = request.form['company_name']
        industry = request.form['industry']
        website = request.form['website']
        city = request.form['city']
        state = request.form['state']
        notes = request.form.get('notes', '')

        cursor.execute('''
            UPDATE companies 
            SET company_name = %s, industry = %s, website = %s, city = %s, state = %s, notes = %s
            WHERE company_id = %s
        ''', (company_name, industry, website, city, state, notes, company_id))

        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('companies'))

    cursor.execute('SELECT * FROM companies WHERE company_id = %s', (company_id,))
    company = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_company.html', company=company)


@app.route('/jobs')
def jobs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Clean query using only columns that exist in your database table
    cursor.execute('''
        SELECT 
            j.job_id,
            j.job_title,
            j.job_type,
            c.company_name 
        FROM jobs j 
        LEFT JOIN companies c ON j.company_id = c.company_id
    ''')
    jobs_list = cursor.fetchall()

    # Get companies for dropdown
    cursor.execute('SELECT company_id, company_name FROM companies')
    companies_list = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('jobs.html', jobs=jobs_list, companies=companies_list)


@app.route('/add_job', methods=['POST'])
def add_job():
    company_id = request.form['company_id']
    job_title = request.form['title']  # matches form input name="title"
    job_type = request.form['job_type']
    salary_range = request.form['salary_range']
    description = request.form['description']
    skills_required = request.form['skills_required']

    conn = get_db_connection()
    cursor = conn.cursor()
    # Updated to use job_title instead of title, and removed location
    cursor.execute('''
        INSERT INTO jobs (company_id, job_title, job_type, salary_range, description, skills_required)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (company_id, job_title, job_type, salary_range, description, skills_required))

    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('jobs'))


@app.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        company_id = request.form['company_id']
        job_title = request.form['title']
        job_type = request.form['job_type']
        salary_range = request.form['salary_range']
        description = request.form['description']
        skills_required = request.form['skills_required']

        # Updated to use job_title, and removed location
        cursor.execute('''
            UPDATE jobs 
            SET company_id = %s, job_title = %s, job_type = %s, 
                salary_range = %s, description = %s, skills_required = %s
            WHERE job_id = %s
        ''', (company_id, job_title, job_type, salary_range, description, skills_required, job_id))

        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('jobs'))

    cursor.execute('SELECT * FROM jobs WHERE job_id = %s', (job_id,))
    job = cursor.fetchone()

    cursor.execute('SELECT company_id, company_name FROM companies')
    companies_list = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('edit_job.html', job=job, companies=companies_list)


@app.route('/delete_job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM jobs WHERE job_id = %s', (job_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('jobs'))


@app.route('/applications')
def applications():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Query applications joining jobs and companies with verified columns
    cursor.execute('''
        SELECT 
            a.application_id,
            a.status,
            a.notes,
            j.job_title,
            c.company_name
        FROM applications a
        LEFT JOIN jobs j ON a.job_id = j.job_id
        LEFT JOIN companies c ON j.company_id = c.company_id
    ''')
    apps_list = cursor.fetchall()

    # Get jobs for dropdown in the Add Application form
    cursor.execute('''
        SELECT j.job_id, j.job_title, c.company_name 
        FROM jobs j 
        LEFT JOIN companies c ON j.company_id = c.company_id
    ''')
    jobs_list = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('applications.html', applications=apps_list, jobs=jobs_list)


@app.route('/add_application', methods=['POST'])
def add_application():
    job_id = request.form['job_id']
    status = request.form['status']
    notes = request.form.get('notes', '')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO applications (job_id, status, notes)
        VALUES (%s, %s, %s)
    ''', (job_id, status, notes))

    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('applications'))


@app.route('/delete_application/<int:application_id>', methods=['POST'])
def delete_application(application_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM applications WHERE application_id = %s', (application_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('applications'))

@app.route('/search_jobs', methods=['GET', 'POST'])
def search_jobs():
    search_query = ''
    if request.method == 'POST':
        search_query = (
            request.form.get('query') or
            request.form.get('search') or
            request.form.get('keyword') or
            request.form.get('q') or
            request.form.get('term') or ''
        )
        if not search_query and request.form:
            search_query = list(request.form.values())[0]
    else:
        search_query = (
            request.args.get('query') or
            request.args.get('search') or
            request.args.get('keyword') or
            request.args.get('q') or
            request.args.get('term') or ''
        )
        if not search_query and request.args:
            search_query = list(request.args.values())[0]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if not str(search_query).strip():
        jobs_list = []
    else:
        # Only query columns that officially exist in your database table
        query = """
            SELECT j.job_id, j.job_title, j.job_type, c.company_name 
            FROM jobs j
            JOIN companies c ON j.company_id = c.company_id
            WHERE j.job_title LIKE %s OR j.job_type LIKE %s
        """
        like_param = f"%{search_query}%"
        cursor.execute(query, (like_param, like_param))
        jobs_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('search_jobs.html', jobs=jobs_list, search_query=search_query)




if __name__ == '__main__':
    app.run(debug=True)
