from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(32), nullable=False)  # admin | teacher | student
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    roll_no = db.Column(db.String(50), unique=True)
    batch = db.Column(db.String(50))
    user = db.relationship('User', backref='student_profile')

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    department = db.Column(db.String(100))
    user = db.relationship('User', backref='teacher_profile')

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(200), nullable=False)

class Classroom(db.Model):
    __tablename__ = 'classrooms'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True)
    capacity = db.Column(db.Integer)

class Slot(db.Model):
    __tablename__ = 'slots'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id', ondelete='SET NULL'), nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'), nullable=True)
    day_of_week = db.Column(db.Integer, nullable=False)  # 1..5
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    current_enrollment = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)

    subject = db.relationship('Subject')
    teacher = db.relationship('Teacher')
    classroom = db.relationship('Classroom')

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'))
    slot_id = db.Column(db.Integer, db.ForeignKey('slots.id', ondelete='CASCADE'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='CASCADE'))
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('Student')
    slot = db.relationship('Slot')
    subject = db.relationship('Subject')
