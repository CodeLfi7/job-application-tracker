# Job Application Tracker (COP4751 Course Project)

A full-stack web application designed to help job seekers efficiently manage companies, job listings, application tracking statuses, and dynamic skill matching. Developed for **COP4751 - Advanced Database Management**.

## Tech Stack
* **Backend:** Python, Flask
* **Database Management:** MySQL (`mysql-connector-python`) with relational foreign keys and schema constraints
* **Frontend:** HTML5, CSS3, Bootstrap 5

## Project Structure
* `app.py`: Main Flask application file containing all routes and view functions.
* `db_connection.py`: Handles MySQL database configuration and connection logic.
* `job_tracker_db.py` / scripts: Database initialization and management scripts.
* `requirements`: Python package dependencies.
* `templates/`: HTML templates styled with Bootstrap for dashboards, companies, jobs, applications, and search.

---

## Setup and Testing Instructions for Instructors

Follow these steps to clone and run the application locally:

### - Clone the Repository
```bash
git clone [https://github.com/CodeLfi7/job-application-tracker.git](https://github.com/CodeLfi7/job-application-tracker.git)
cd job-application-tracker
python3 -m venv .venv
source .venv/bin/activate    # On Windows use: .venv\Scripts\activate
pip install -r requirements
CREATE DATABASE job_tracker;
python job_tracker_db.py
python app.py
Open your web browser and navigate to:
http://127.0.0.1:5000
Project Demo Video
Watch the full 5:26 project demo and walkthrough: https://youtu.be/cdqnmC-tJwg 

