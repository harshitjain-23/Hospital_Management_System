from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from app import db
from app.models.login import login
from app.models.doctor import doctor
from app.models.patient import patient

login = Blueprint('sign-in', __name__)


# Client / User Login
@login.route('/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = login.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_email'] = user.email
            session['role'] = user.role

            flash("Login successful!", "success")

            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'doctor':
                return redirect(url_for('doctor.dashboard'))
            elif user.role == 'patient':
                return redirect(url_for('patient.dashboard'))
            else:
                flash("Invalid role!", "danger")
                return redirect(url_for('sign-in.login'))
        else:
            flash("Invalid username or password!", "danger")
            return redirect(url_for('sign-in.login'))

    return render_template('sign-in.html')

@login.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('sign-in.login'))

@login.route('/forgot-password', methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = login.query.filter_by(email=email).first()

        if user:
            flash("Password reset link sent to your email.", "info")
            # Implement actual email sending logic here
        else:
            flash("Email not found!", "danger")

    return render_template('forgot-password.html')

@login.route('/reset-password/<token>', methods=["GET", "POST"])
def reset_password(token):
    # Token verification logic should be implemented here
    if request.method == "POST":
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if new_password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('sign-in.reset_password', token=token))

        # Assuming token is valid and we can get user email from it
        user_email = "
        user = login.query.filter_by(email=user_email).first()
        if user:
            user.password = new_password  # In production, hash the password
            db.session.commit()
            flash("Password reset successful!", "success")
            return redirect(url_for('sign-in.login'))
        else:
            flash("Invalid token!", "danger")
            return redirect(url_for('sign-in.forgot_password'))
        return render_template('reset-password.html', token=token)
    
@login.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = "patient"

        if login.query.filter_by(email=email).first():
            flash("Email already registered!", "danger")
            return redirect(url_for('sign-in.register'))

        new_user = login(email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('sign-in.login'))

    return render_template('register.html')