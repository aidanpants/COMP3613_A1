import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import (User, Shortlist, Position, Staff, Student, Employer)
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )



app = create_app()
migrate = get_migrate(app)

@app.cli.command("init", help="Creates and initializes the database")
def init():
    # Clear all tables if needed (optional)
    db.drop_all()
    db.create_all()

    user = User(username='jaden', password='jadenpass')
    employer = Employer(name='First Citezens Bank')
    staff = Staff(name='Beatrix')
    student = Student(name='Bill')
    position = Position(name="Intern", description="Internship position", employer=employer)
    shortlist = Shortlist(student=student, position=position, status='pending', staff=staff)

    db.session.add_all([user, employer, staff, student, position, shortlist])
    db.session.commit()
    print('Database initialized')


'''
User Commands
'''
    
user_cli = AppGroup('user', help='User object commands') 

@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')


@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli)


@app.cli.command("view-shortlist")
@click.argument("position_id")
def view_shortlist(position_id):
    """View all students in the shortlist for a position"""
    position = Position.query.get(position_id)
    if not position:
        print(f"Position with ID {position_id} not found")
        return

    shortlists = Shortlist.query.filter_by(position_id=position_id).all()
    if not shortlists:
        print(f"No students in shortlist for position {position.name}")
        return

    print(f"Shortlist for position {position.name}:")
    for s in shortlists:
        student = Student.query.get(s.student_id)
        staff = Staff.query.get(s.staff_id)
        print(f"Student: {student.name} | Added by Staff: {staff.name} | Status: {s.status}")


'''
Employer Commands
'''
@app.cli.command("create-position")
@click.argument("position_id")
@click.argument("employer_id")
@click.argument("title")
def create_position(position_id, employer_id, title):
    existing = Position.query.get(position_id)
    if existing:
        print(f"Position with ID {position_id} already exists: {existing.name}")
        return
    
    employer = Employer.query.get(employer_id)
    if not employer:
        print(f"Employer with ID {employer_id} not found")
        return

    position = Position(
        position_id=position_id,
        name=title,
        description="Internship position",
        employer_id=employer_id
    )
    db.session.add(position)
    db.session.commit()
    print(f"Position {position.name} created for Employer {employer.name} with ID {position.position_id}")


@app.cli.command("update-status")
@click.argument("position_id")
@click.argument("student_id")
@click.argument("status")
def update_status(position_id, student_id, status): 
    if status.lower() not in ["accepted", "rejected", "pending"]:
        print("Status must be 'accepted', 'rejected', or 'pending'")
        return

    shortlist_entry = Shortlist.query.filter_by(position_id=position_id, student_id=student_id).first()
    if not shortlist_entry:
        print(f"Student with ID {student_id} is not in the shortlist for position {position_id}")
        return

    shortlist_entry.status = status.lower()
    db.session.commit()
    student = Student.query.get(student_id)
    position = Position.query.get(position_id)
    print(f"Student {student.name} status updated to '{status}' for position {position.name}")



'''
Staff Commands
'''
@app.cli.command("add-student")
@click.argument("staff_id")
@click.argument("student_id")
@click.argument("position_id")
def add_to_shortlist(staff_id, student_id, position_id):
    staff = Staff.query.get(staff_id)
    student = Student.query.get(student_id)
    position = Position.query.get(position_id)

    if not all([staff, student, position]):
        print("Invalid staff, student, or position ID")
        return

    shortlist_entry = Shortlist(
        staff_id=staff_id,
        student_id = student_id,
        position_id = position_id,
        status="pending"
    )
    db.session.add(shortlist_entry)
    db.session.commit()
    print(f"Student {student.name} added to shortlist for Position {position.name} by Staff {staff.name}")


'''
Student Commands
'''
@app.cli.command("student-shortlist")
@click.argument("student_id")
def student_shortlist(student_id):
    """View all positions a student is shortlisted for, with employer response"""
    student = Student.query.get(student_id) 
    if not student:
        print(f"Student with ID {student_id} not found")
        return

    shortlists = Shortlist.query.filter_by(student_id=student_id).all()
    if not shortlists:
        print(f"Student {student.name} is not shortlisted for any positions")
        return

    print(f"Shortlisted positions for {student.name}:")
    for s in shortlists:
        position = Position.query.get(s.position_id)
        employer = Employer.query.get(position.employer_id)
        print(f"Position: {position.name} | Employer: {employer.name} | Status: {s.status}")

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)