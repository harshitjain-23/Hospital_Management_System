from app import db

class login(db.Model):
    __tablename__ = 'login'
    email = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100), nullable=False) 
    role = db.Column(db.String(50), nullable=False)

try:
    if not login.query(role="superuser").first():
        default_admin = login(email="admin@gmail.com", password="admin123", role="superuser")
        db.session.add(default_admin)
        db.session.commit()
        print("Default superuser created.")
    else:
        print("Superuser already exists.")
        
except Exception as e:
    print("Error checking/creating superuser:", e)
    db.session.rollback()


    def check_password(self, password):
        return self.password == password 
    # In production, use hashed passwords


