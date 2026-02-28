📚 Slot-Based Timetable & Enrollment Management System

This project is a web-based academic scheduling and course enrollment system developed using Flask, SQLAlchemy, and Flask-Login. The system provides role-based access for Admin, Students, and Teachers to manage subjects, timetable slots, classroom allocation, and student enrollments efficiently.

The application simulates a mini college ERP module where administrators can create and manage academic resources, students can enroll in available course slots without time conflicts, and teachers can view their assigned schedules.

🚀 Features
🔐 Authentication & Authorization

Secure login and registration system

Password hashing for security

Role-based access control (Admin / Teacher / Student)

👨‍💼 Admin Module

Add and manage subjects

Add teachers and classrooms

Create timetable slots with capacity limits

View structured timetable dashboard

Seed demo data for testing

🎓 Student Module

Register and login

View available subject slots

Enroll in preferred slots

Automatic time conflict detection

Capacity validation for slots

Prevent duplicate subject enrollment

View enrolled subjects

👩‍🏫 Teacher Module

Login and access personalized dashboard

View assigned teaching slots and schedule

🧠 Key Functionalities

Slot-based timetable management

Real-time enrollment capacity tracking

Time conflict detection algorithm

Database relationship management using ORM

Transaction-safe enrollment handling

Clean MVC-style Flask architecture

🛠️ Tech Stack

Backend: Python, Flask

Database: SQLite / PostgreSQL (configurable)

ORM: SQLAlchemy

Authentication: Flask-Login

Frontend: HTML, CSS, Jinja2 Templates

Security: Werkzeug password hashing

📂 Database Entities

Users

Students

Teachers

Subjects

Classrooms

Slots (Timetable)

Enrollments

🎯 Use Cases

College elective selection systems

Lab batch allocation

Academic timetable management

Coaching institute scheduling platforms

⭐ Learning Outcomes

This project demonstrates:

Full-stack web development using Flask

Database design and relational modeling

Authentication and session management

Role-based system architecture

Real-world scheduling logic implementation

📌 Future Enhancements

Drag-and-drop timetable interface

Email notifications for enrollment

Attendance tracking module

REST API integration

Admin analytics dashboard
