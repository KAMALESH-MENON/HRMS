# HRMS Web Application

This Flask web application manages employee information and attendance.

## Project Structure

- `app.py`: Main application file.
- `models.py`: SQLAlchemy models for the database.
- `static/`: Folder containing static files (CSS).
- `templates/`: Folder containing HTML templates.

## How to Run Locally

1. Clone the repository:

    git clone https://github.com/KAMALESH-MENON/HRMS.git

2. Install dependencies:

    pip install -r requirements.txt

3. Set up the database URI in the environment or update `app.py` with your database details.

4. Run the application:

    python app.py

5. Access the application in your browser: [http://localhost:5000](http://localhost:5000)

## Database Schema
The HRMS (Human Resource Management System) utilizes a simple relational database schema with two main entities: employees and attendance_records. The schema is implemented using SQLAlchemy, and the model classes are defined as follows:

- Employee

    id (Primary Key): Unique identifier for each employee.
    name: Name of the employee (String, 80 characters, non-nullable).
    designation: Designation or job title of the employee (String, 50 characters).
    department: Department to which the employee belongs (String, 50 characters).
    date_joined: Date when the employee joined the company (Date, non-nullable).

- Attendance

    id (Primary Key): Unique identifier for each attendance record.
    in_time: Timestamp indicating the time when the employee checked in (DateTime, non-nullable, default is the current UTC time).
    out_time: Timestamp indicating the time when the employee checked out (DateTime, nullable).
    employee_id (Foreign Key): Relates each attendance record to a specific employee.

## Design Decisions

   - Serialization: Both Employee and Attendance classes include a serialize method to easily convert the objects to a dictionary. This is useful for JSON serialization when providing data through API endpoints or rendering templates.

   - Relationships: The Employee and Attendance classes are linked through a one-to-many relationship. An employee can have multiple attendance records, but each attendance record is associated with a single employee.

   - Default Values: The in_time attribute in the Attendance class has a default value of the current UTC time. This ensures that if the check-in time is not provided explicitly, it defaults to the current time.

   - Back-populates Relationship: The relationship attribute back_populates is used to correctly define the bidirectional relationship between Employee and Attendance. This ensures consistency when navigating the relationships from either side.
