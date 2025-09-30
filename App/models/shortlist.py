from App.database import db

class Shortlist(db.Model):
    __tablename__ = "shortlist"
    shortlist_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, nullable=False)
    
    employer_id = db.Column(db.String, db.ForeignKey('employer.employer_id'))
    student_id = db.Column(db.String, db.ForeignKey('student.student_id'))
    staff_id = db.Column(db.String, db.ForeignKey('staff.staff_id'))
    position_id = db.Column(db.String, db.ForeignKey('position.position_id'))

    staff = db.relationship("Staff", back_populates="shortlists")
    student = db.relationship("Student", back_populates="shortlists")
    position = db.relationship("Position", back_populates="shortlists")