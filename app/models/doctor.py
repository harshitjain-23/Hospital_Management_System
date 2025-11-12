from app import db

class doctor(db.Model):
    __tablename__ = 'doctor'
    d_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    education = db.Column(db.String(200), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.String(200), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    fees = db.Column(db.Float, nullable=False)
    timings = db.Column(db.String(100), nullable=False)
    days_available = db.Column(db.String(100), nullable=False)
    profile_image = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(50), nullable=False, default='active')
    
    def __repr__(self):
        return f"<Doctor {self.name} - {self.specialization}>"
    

