from app import db

class treatment(db.Model):
    __tablename__ = 'treatment'
    t_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    a_id = db.Column(db.Integer, db.ForeignKey('appointment.a_id'), nullable=False)
    p_id = db.Column(db.Integer, db.ForeignKey('patient.p_id'), nullable=False)
    d_id = db.Column(db.Integer, db.ForeignKey('doctor.d_id'), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    prescription = db.Column(db.Text, nullable=False)
    follow_up_date = db.Column(db.Date, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='ongoing') # (ongoing/completed)

    # backref relationships
    appointment = db.relationship('appointment', backref=db.backref('treatments', lazy=True))
    patient = db.relationship('patient', backref=db.backref('treatments', lazy=True))
    doctor = db.relationship('doctor', backref=db.backref('treatments', lazy=True))
    

    def __repr__(self):
        return f"<Treatment {self.t_id} - Patient {self.p_id} with Doctor {self.d_id}>"
    