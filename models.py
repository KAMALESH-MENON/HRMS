from sqlalchemy import Column, Integer, DateTime, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    designation = Column(String(50))
    department = Column(String(50))
    date_joined = Column(Date, nullable=False)

    attendances = relationship('Attendance', back_populates='employee')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'designation': self.designation,
            'department': self.department,
            'date_joined': str(self.date_joined),  # Convert Date to string for serialization
        }

class Attendance(Base):
    __tablename__ = 'attendance_records'

    id = Column(Integer, primary_key=True)
    in_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    out_time = Column(DateTime)
    employee_id = Column(Integer, ForeignKey('employees.id'))

    # Correct the back_populates attribute to match the relationship name in Employee
    employee = relationship('Employee', back_populates='attendances')

    def serialize(self):
        return {
            'id': self.id,
            'in_time': str(self.in_time),
            'out_time': str(self.out_time) if self.out_time else None,
            'employee_id': self.employee_id,
        }