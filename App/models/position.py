from App.database import db

class Position(db.Model):
    __tablename__ = "position"
    position_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255))

    employer_id = db.Column(db.String, db.ForeignKey("employer.employer_id"), nullable=False)

    employer = db.relationship("Employer", back_populates="positions")
    shortlists = db.relationship("Shortlist", back_populates="position")    