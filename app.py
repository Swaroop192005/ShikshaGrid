import os
from datetime import time
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Student, Teacher, Subject, Classroom, Slot, Enrollment
from config import DATABASE_URL, SECRET_KEY
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        if current_user.role == 'teacher':
            return redirect(url_for('teacher_dashboard'))
        return redirect(url_for('student_dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        if not full_name or not email or not password:
            flash('Please fill all fields', 'danger')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'warning')
            return redirect(url_for('register'))
        hashed = generate_password_hash(password)
        user = User(full_name=full_name, email=email, password=hashed, role='student')
        db.session.add(user)
        db.session.flush()
        student = Student(user_id=user.id, roll_no=f'R{user.id:04d}', batch='CE-5')
        db.session.add(student)
        db.session.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully', 'success')
            return redirect(url_for('index'))
        flash('Invalid credentials', 'danger')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('login'))

# Add Subject
@app.route('/admin/add_subject', methods=['POST'])
@login_required
def add_subject():
    if current_user.role != 'admin': return jsonify({'error':'forbidden'}),403
    code = request.form.get('code')
    name = request.form.get('name')
    if Subject.query.filter_by(code=code).first():
        flash('Subject code exists', 'warning'); return redirect(url_for('admin_dashboard'))
    db.session.add(Subject(code=code,name=name)); db.session.commit()
    flash('Subject added','success'); return redirect(url_for('admin_dashboard'))

# Add Slot
@app.route('/admin/add_slot', methods=['POST'])
@login_required
def add_slot():
    if current_user.role != 'admin': return jsonify({'error':'forbidden'}),403
    s = Slot(
        subject_id=int(request.form.get('subject_id')),
        teacher_id=int(request.form.get('teacher_id')),
        classroom_id=int(request.form.get('classroom_id')),
        day_of_week=int(request.form.get('day_of_week')),
        start_time=request.form.get('start_time'),
        end_time=request.form.get('end_time'),
        max_capacity=int(request.form.get('max_capacity')),
    )
    db.session.add(s); db.session.commit()
    flash('Slot added','success'); return redirect(url_for('admin_dashboard'))

@app.route('/admin/add_teacher', methods=['POST'])
@login_required
def add_teacher():
    if current_user.role != 'admin':
        return jsonify({'error':'forbidden'}), 403
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    department = request.form.get('department')
    password = request.form.get('password')

    if User.query.filter_by(email=email).first():
        flash('Email already exists', 'warning')
        return redirect(url_for('admin_dashboard'))

    hashed = generate_password_hash(password)
    user = User(full_name=full_name, email=email, password=hashed, role='teacher')
    db.session.add(user)
    db.session.flush()  # get user.id before commit
    teacher = Teacher(user_id=user.id, department=department)
    db.session.add(teacher)
    db.session.commit()

    flash('Teacher added successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add_classroom', methods=['POST'])
@login_required
def add_classroom():
    if current_user.role != 'admin':
        return jsonify({'error':'forbidden'}), 403
    code = request.form.get('code')
    capacity = request.form.get('capacity')

    if Classroom.query.filter_by(code=code).first():
        flash('Classroom code already exists', 'warning')
        return redirect(url_for('admin_dashboard'))

    classroom = Classroom(code=code, capacity=int(capacity))
    db.session.add(classroom)
    db.session.commit()

    flash('Classroom added successfully', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/seed', methods=['POST'])
@login_required
def admin_seed():
    if current_user.role != 'admin':
        return jsonify({'error':'forbidden'}), 403
    try:
        # avoid reseed if subjects exist
        if Subject.query.first():
            return jsonify({'msg':'already seeded'}), 200

        # create demo users
        admin = User(full_name='Admin', email='admin@sg.com', password=generate_password_hash('admin123'), role='admin')
        t1 = User(full_name='Mahesh Khandke', email='mahesh@sg.com', password=generate_password_hash('teach123'), role='teacher')
        t2 = User(full_name='Divya Surve', email='divya@sg.com', password=generate_password_hash('teach123'), role='teacher')
        s1 = User(full_name='Demo Student', email='student@sg.com', password=generate_password_hash('stud123'), role='student')

        db.session.add_all([admin, t1, t2, s1])
        db.session.flush()
        db.session.add_all([Teacher(user_id=t1.id, department='CE'), Teacher(user_id=t2.id, department='CE'), Student(user_id=s1.id, roll_no='R0001', batch='CE-5')])
        db.session.commit()

        # subjects & classrooms
        subjects = [
            Subject(code='SE', name='Software Engineering'),
            Subject(code='DS', name='Distributed Systems'),
            Subject(code='SPCD', name='System Programs & Compiler Design'),
            Subject(code='AI', name='Artificial Intelligence'),
            Subject(code='DWM', name='Data Warehousing & Mining'),
        ]
        db.session.add_all(subjects)
        db.session.add_all([Classroom(code='M206', capacity=75), Classroom(code='M302', capacity=75), Classroom(code='L101', capacity=60)])
        db.session.flush()
        teachers = Teacher.query.all()
        rooms = Classroom.query.all()
        subs = Subject.query.all()

        # slots
        db.session.add_all([
            Slot(subject_id=subs[3].id, teacher_id=teachers[0].id, classroom_id=rooms[0].id, day_of_week=1, start_time=time(9,0), end_time=time(11,0), max_capacity=70),
            Slot(subject_id=subs[0].id, teacher_id=teachers[1].id, classroom_id=rooms[1].id, day_of_week=1, start_time=time(9,0), end_time=time(11,0), max_capacity=70),
            Slot(subject_id=subs[1].id, teacher_id=teachers[0].id, classroom_id=rooms[2].id, day_of_week=2, start_time=time(11,0), end_time=time(13,0), max_capacity=70),
        ])
        db.session.commit()
        return jsonify({'msg':'seeded'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}), 500

from collections import defaultdict

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('forbidden', 'danger')
        return redirect(url_for('index'))

    slots = Slot.query.all()
    subjects = Subject.query.all()
    teachers = Teacher.query.all()
    classrooms = Classroom.query.all()

    # Prepare timetable dict: timetable[day][start_time] = slot
    timetable = defaultdict(dict)
    for s in slots:
        timetable[s.day_of_week][s.start_time.strftime('%H:%M')] = s

    return render_template(
        'admin_dashboard.html',
        slots=slots,
        subjects=subjects,
        teachers=teachers,
        classrooms=classrooms,
        timetable=timetable
    )


@app.route('/student')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash('forbidden', 'danger')
        return redirect(url_for('index'))
    slots = Slot.query.all()
    enrolls = Enrollment.query.join(Student, Enrollment.student_id == Student.id).filter(Student.user_id == current_user.id).all()
    return render_template('student_dashboard.html', slots=slots, enrolls=enrolls)

@app.route('/enroll', methods=['POST'])
@login_required
def enroll():
    if current_user.role != 'student':
        return jsonify({'error':'forbidden'}), 403
    slot_id = int(request.form.get('slot_id'))
    student = Student.query.filter_by(user_id=current_user.id).first()
    slot = Slot.query.filter_by(id=slot_id).with_for_update().first()
    if not slot:
        flash('Slot not found', 'danger')
        return redirect(url_for('student_dashboard'))
    # check same subject
    existing = Enrollment.query.filter_by(student_id=student.id, subject_id=slot.subject_id).first()
    if existing:
        flash('Already enrolled in this subject', 'warning')
        return redirect(url_for('student_dashboard'))
    # naive time conflict check
    my_slots = Slot.query.join(Enrollment, Enrollment.slot_id == Slot.id).filter(Enrollment.student_id == student.id).all()
    for s in my_slots:
        if s.day_of_week == slot.day_of_week and not (s.end_time <= slot.start_time or slot.end_time <= s.start_time):
            flash('Time conflict with another enrolled slot', 'danger')
            return redirect(url_for('student_dashboard'))
    if slot.current_enrollment >= slot.max_capacity:
        flash('Slot full', 'warning')
        return redirect(url_for('student_dashboard'))
    enroll = Enrollment(student_id=student.id, slot_id=slot.id, subject_id=slot.subject_id)
    db.session.add(enroll)
    slot.current_enrollment = (slot.current_enrollment or 0) + 1
    db.session.commit()
    flash('Enrolled successfully', 'success')
    return redirect(url_for('student_dashboard'))

@app.route('/teacher')
@login_required
def teacher_dashboard():
    if current_user.role != 'teacher':
        flash('forbidden', 'danger')
        return redirect(url_for('index'))
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    slots = Slot.query.filter_by(teacher_id=teacher.id).all()
    return render_template('teacher_dashboard.html', slots=slots)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
