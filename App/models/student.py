from App.database import db

class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # Relationship: A student can be on multiple shortlists
    shortlists = db.relationship("Shortlist", back_populates="student")

    def viewPosition(self):
        return [s.position for s in self.shortlists]

    def viewResponse(self):
        return [s.status for s in self.shortlists]