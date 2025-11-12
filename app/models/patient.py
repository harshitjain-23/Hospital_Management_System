from app import db

class patient(db.Model):
    __tablename__ = 'patient'
    p_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    contact = db.Column(db.String(15), nullable=False)  
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    medical_history = db.Column(db.Text, nullable=True)
    family_history = db.Column(db.Text, nullable=True)
    allergies = db.Column(db.Text, nullable=True)
    profile_image = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(50), nullable=False, default='active')
    
    def __repr__(self):
        return f"<Patient {self.name} - {self.age} years>"
    