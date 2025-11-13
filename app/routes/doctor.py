from flask import Blueprint, redirect, render_template, request, flash, session, url_for
from app import db
from app.models import doctor, patient, appointment, treatment
from functools import wraps


doctor_bp = Blueprint('doctor', __name__)

def is_doctor_authenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'doctor_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.doctor_login'))
        return f(*args, **kwargs)
    return decorated_function

@doctor_bp.route('/dashboard')
@is_doctor_authenticated
def doctor_dashboard():
    doctor_id = session['doctor_id']
    doc = doctor.query.get(doctor_id)
    # Fetch doctor's appointments and treatments
    appointments = appointment.query.filter_by(doctor_id=doctor_id).all()
    treatments = treatment.query.filter_by(doctor_id=doctor_id).all()
    
    return render_template('doctor/dashboard.html', doctor=doc, appointments=appointments, treatments=treatments)


# Doctor profile route
@doctor_bp.route('/profile', methods=['GET', 'POST'])
@is_doctor_authenticated
def doctor_profile():
    doctor_id = session['doctor_id']
    doc = doctor.query.get(doctor_id)
    
    if request.method == 'POST':
        # Update profile logic
        doc.name = request.form['name']
        doc.specialization = request.form['specialization']
        doc.contact = request.form['contact']
        doc.email = request.form['email']
        doc.address = request.form['address']
        doc.fees = request.form['fees']
        doc.timings = request.form['timings']
        doc.days_available = request.form['days_available']
        doc.education = request.form['education']
        doc.experience = request.form['experience']
        doc.profile_image = request.form['profile_image']
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('doctor.doctor_profile'))
    
    return render_template('doctor/profile.html', doctor=doc)


# View doc Patients route
@doctor_bp.route('/patients')
@is_doctor_authenticated
def view_patients():
    doctor_id = session['doctor_id']
    appointments = appointment.query.filter_by(doctor_id=doctor_id).all()
    patient_ids = {appt.patient_id for appt in appointments}
    patients = patient.query.filter(patient.p_id.in_(patient_ids)).all()
    return render_template('doctor/patients.html', patients=patients)





# Search Patients route using azax
@doctor_bp.route('/search_patients', methods=['GET', 'POST'])
@is_doctor_authenticated
def search_patients():
    doctor_id = session['doctor_id']
    query = request.form.get('query', '')
    appointments = appointment.query.filter_by(doctor_id=doctor_id).all()
    patient_ids = {appt.patient_id for appt in appointments}
    
    patients = patient.query.filter(
        patient.p_id.in_(patient_ids) |
        patient.name.ilike(f'%{query}%') |
        patient.contact.ilike(f'%{query}%') |
        patient.email.ilike(f'%{query}%') |
        patient.address.ilike(f'%{query}%') |
        patient.age.ilike(f'%{query}%') |
        patient.gender.ilike(f'%{query}%') |
        patient.blood_group.ilike(f'%{query}%') |
        patient.medical_history.ilike(f'%{query}%') |
        patient.allergies.ilike(f'%{query}%') |
        patient.current_medications.ilike(f'%{query}%') |
        patient.emergency_contact.ilike(f'%{query}%') |
        patient.insurance_details.ilike(f'%{query}%') 
    ).all()
    
    return render_template('doctor/patient_search_results.html', patients=patients)


# View past, today, upcoming(this week and later seperately) Appointments route
@doctor_bp.route('/appointments')
@is_doctor_authenticated
def view_appointments():
    doctor_id = session['doctor_id']    


    past_appointments = appointment.query.filter(appointment.d_id==doctor_id, appointment.date < db.func.current_date()).all()
    todays_appointments = appointment.query.filter(appointment.d_id==doctor_id, appointment.date += db.func.current_date()).all()
    this_week_appointments = appointment.query.filter(appointment.d_id==doctor_id, appointment.date > db.func.current_date(), appointment.date <= db.func.current_date() + db.func.interval('7 days')).all()
    upcoming_appointments = appointment.query.filter(appointment.d_id==doctor_id, appointment.date > db.func.current_date() + db.func.interval('7 days')).all()

    return render_template('doctor/appointments.html', past_appointments=past_appointments, todays_appointments=todays_appointments, this_week_appointments=this_week_appointments, upcoming_appointments=upcoming_appointments)
    

# add Treatment route and mark appointment as completed

# View patient history route

#

# Update Appointment status route and send mail to patient
@doctor_bp.route('/update_appointment/<int:appointment_id>', methods=['POST'])
@is_doctor_authenticated
def update_appointment(appointment_id):
    appt = appointment.query.get(appointment_id)
    if not appt:
        flash('Appointment not found.', 'danger')
        return redirect(url_for('doctor.view_appointments'))
    
    new_status = request.form['status']
    appt.status = new_status
    db.session.commit()
    
    # Logic to send email to patient about status update can be added here
    
    flash('Appointment status updated successfully!', 'success')
    return redirect(url_for('doctor.view_appointments'))



# Set Availability route
@doctor_bp.route('/set_availability', methods=['GET', 'POST'])
@is_doctor_authenticated
def set_availability():
    doctor_id = session['doctor_id']
    doc = doctor.query.get(doctor_id)
    
    if request.method == 'POST':
        doc.days_available = request.form['days_available']
        doc.timings = request.form['timings']
        db.session.commit()
        flash('Availability updated successfully!', 'success')
        return redirect(url_for('doctor.set_availability'))
    
    return render_template('doctor/set_availability.html', doctor=doc)