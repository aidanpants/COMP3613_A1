from App.database import db
from App.models.shortlist import Shortlist
from App.models.position import Position
from App.models.student import Student

class Staff(db.Model):
    __tablename__ = "staff"
    staff_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    shortlists = db.relationship("Shortlist", back_populates="staff")

    def add_to_shortlist(self, student_id, position_id):
        student = Student.query.get(student_id)
        position = Position.query.get(position_id)
        if not student or not position:
            raise ValueError("Student or Position not found")

        # Create shortlist entry
        shortlist_entry = Shortlist(
            student_id = student.student_id,
            position_id = position.position_id,
            staff_id = self.staff_id,
            status ='pending'
        )

        db.session.add(shortlist_entry)
        db.session.commit()
        return shortlist_entry
