from app import db

class appointment(db.Model):
    __tablename__ = 'appointment'
    a_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    p_id = db.Column(db.Integer, db.ForeignKey('patient.p_id'), nullable=False)
    d_id = db.Column(db.Integer, db.ForeignKey('doctor.d_id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='scheduled') # (Booked/Completed/Cancelled)
    notes = db.Column(db.Text, nullable=True)

    # backref relationships
    patient = db.relationship('patient', backref=db.backref('appointments', lazy=True))
    doctor = db.relationship('doctor', backref=db.backref('appointments', lazy=True))
    

    def __repr__(self):
        return f"<Appointment {self.id} - {self.patient_name} with {self.doctor_name} on {self.appointment_date}>"