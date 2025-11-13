from app import db

class doctor(db.Model):
    __tablename__ = 'doctor'
    d_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    education = db.Column(db.String(200), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.String(200), nullable=True)
    contact = db.Column(db.String(15), nullable=False , unique=True)
    email = db.Column(db.String(100), nullable=False , unique=True)
    address = db.Column(db.String(200), nullable=True)
    fees = db.Column(db.Float, nullable=True)
    timings = db.Column(db.String(100), nullable=True)
    days_available = db.Column(db.String(100), nullable=True)
    profile_image = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(50), nullable=False, default='active') # e.g., active, inactive, blacklisted
    
    def __repr__(self):
        return f"<Doctor {self.name} - {self.specialization}>"