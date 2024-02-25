from flask import Flask, request, render_template, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from models import Base, Employee, Attendance
import os
from datetime import datetime


# Load configuration from environment variables
app = Flask(__name__)
DATABASE_URI = os.environ.get('DATABASE_URI', 'mysql://root:12345678@localhost/hrms_db')

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(engine)  # Create tables if not already present

@app.route('/')
def index():
    """
    Render the index page with a list of all employees.

    Returns:
        HTML template: Rendered HTML template.
    """
    session = SessionLocal()
    employees = session.query(Employee).all()
    session.close()
    return render_template('index.html', employees=employees)

@app.route('/employees', methods=['GET', 'POST'])
def employees():
    """
    Render the employees page with a list of all employees.
    Handles both GET and POST requests.

    Returns:
        HTML template or JSON response: Rendered HTML template or JSON response.
    """
    session = SessionLocal()

    if request.method == 'GET':
        employees = session.query(Employee).all()
        return render_template('employees.html', employees=employees)

    elif request.method == 'POST':
        data = request.get_json()
        new_employee = Employee(
            name=data['name'],
            designation=data['designation'],
            department=data['department'],
            date_joined=data['date_joined']
        )
        session.add(new_employee)
        session.commit()
        session.close()
        return jsonify({'message': 'Employee created successfully.'})

    else:
        session.close()
        return jsonify({'error': 'Invalid request method.'})

@app.route('/employee/<int:employee_id>')
def employee_details(employee_id):
    """
    Render the employee details page for a specific employee.

    Args:
        employee_id (int): The unique identifier for the employee.

    Returns:
        HTML template or JSON response: Rendered HTML template or JSON response.
    """
    session = SessionLocal()

    # Retrieve the employee
    employee = session.query(Employee).get(employee_id)

    if not employee:
        return jsonify({'error': 'Employee not found'}), 404

    # Retrieve the attendance records for the employee
    attendance_records = session.query(Attendance).filter_by(employee_id=employee.id).all()

    session.close()

    return render_template('employee_details.html', employee=employee, attendance=attendance_records)

@app.route('/mark_attendance/<int:employee_id>', methods=['POST'])
def mark_attendance(employee_id):
    session = SessionLocal()

    employee = session.query(Employee).get(employee_id)

    if not employee:
        session.close()
        return jsonify({'error': 'Employee not found'}), 404

    data = request.get_json()
    in_time = data.get('in_time')
    out_time = data.get('out_time')

    # Validate input
    if not in_time:
        session.close()
        return jsonify({'error': 'In-time is required'}), 400

    # Create new attendance record
    new_attendance = Attendance(
        in_time=datetime.strptime(in_time, '%Y-%m-%dT%H:%M:%S'),
        out_time=datetime.strptime(out_time, '%Y-%m-%dT%H:%M:%S') if out_time else None,
        employee_id=employee.id
    )

    session.add(new_attendance)
    session.commit()
    session.close()

    return jsonify({'message': 'Attendance marked successfully'})

@app.route('/attendance/<int:employee_id>', methods=['GET'])
def get_attendance(employee_id):
    """
    Mark attendance for a specific employee on a given date.

    Args:
        employee_id (int): The unique identifier for the employee.

    Returns:
        JSON response: Response indicating the success or failure of marking attendance.
    """
    session = SessionLocal()

    # Retrieve the employee
    employee = session.query(Employee).get(employee_id)

    if not employee:
        session.close()
        return jsonify({'error': 'Employee not found'}), 404

    # Retrieve the attendance records for the employee
    attendance_records = session.query(Attendance).filter_by(employee_id=employee.id).all()

    session.close()

    # Convert the attendance records to a list of serialized dictionaries
    serialized_attendance = [{'id': record.id, 'in_time': str(record.in_time), 'out_time': str(record.out_time) if record.out_time else None} for record in attendance_records]

    return jsonify({'employee': employee.serialize(), 'attendance': serialized_attendance})


@app.route('/report')
def report():
    """
    Generate and display a report on the department-wise employee count.

    Returns:
        HTML response: Rendered template displaying the department-wise employee count.
    """
    session = SessionLocal()

    # Logic to count employees in each department
    departments = session.query(Employee.department).distinct()
    report_data = {department[0]: session.query(Employee).filter_by(department=department[0]).count() for department in departments}

    session.close()
    return render_template('report.html', report_data=report_data)

if __name__ == '__main__':
    app.run(debug=True)
