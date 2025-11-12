from app import db

class department(db.Model):
    __tablename__ = 'department'
    dept_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    head = db.Column(db.String(100), nullable=True)  # Head of Department
    contact = db.Column(db.String(15), nullable=False)
    registered-doctor-ids = db.Column(db.Text, nullable=True)  # Comma-separated list of doctor IDs
    status = db.Column(db.String(50), nullable=False, default='active')  # (active/inactive)

    # backref relationships
    doctors = db.relationship('doctor', backref='department', lazy=True)
 

    def __repr__(self):
        return f"<Department {self.name} - Head: {self.head}>"