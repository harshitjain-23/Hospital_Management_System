from app import db

class patient(db.Model):
    __tablename__ = 'patient'
    p_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    contact = db.Column(db.String(15), nullable=False , unique=True)  
    email = db.Column(db.String(100), nullable=False , unique=True)
    address = db.Column(db.String(200), nullable=False)
    medical_history = db.Column(db.Text, nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    family_history = db.Column(db.Text, nullable=False)
    allergies = db.Column(db.Text, nullable=False)
    profile_image = db.Column(db.String(200), nullable=False)
    insurance_details = db.Column(db.Text, nullable=False)
    current_medications = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='active') 
    
    def __repr__(self):
        return f"<Patient {self.name} - {self.age} years>"
    