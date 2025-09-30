from App.database import db
from App.models.position import Position

class Employer(db.Model):
    __tablename__ = "employer"
    employer_id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String, nullable=False)

    positions = db.relationship("Position", back_populates="employer")


    def createPosition(self, id, name, description):    
        position = Position(
            position_id = id,
            name=name,
            description=description,
            employer_id=self.employer_id
        )   
        db.session.add(position)
        db.session.commit() 
        return position

    def setStatus(self, shortlist, status):
        shortlist.status = status
        db.session.commit()
