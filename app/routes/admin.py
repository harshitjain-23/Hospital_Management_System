from flask import Blueprint, redirect, render_template, request, flash, session, url_for
from app import db
from app.models import login, doctor, patient, appointment, treatment
from functools import wraps  # wraps used for decorator in user authentication


admin_bp = Blueprint('admin', __name__)

# code to check authentication use wrapper function
def is_admin_authenticated():
    @wraps
    def wrapper(*args, **kwargs):
        if 'user_email' in session and session.get('role') == 'admin':
            return True
        return False
    return wrapper()

    
# Admin Dashboard Route with verification through wrapper function
@admin_bp.route('/dashboard')
@is_admin_authenticated
def dashboard():
    total_doctors = doctor.query.count()
    total_patients = patient.query.count()
    total_appointments = appointment.query.count()
    total_treatments = treatment.query.count()

    return render_template('admin/dashboard.html', 
                           total_doctors=total_doctors,
                           total_patients=total_patients,
                           total_appointments=total_appointments,
                           total_treatments=total_treatments)

# Manage Doctors Route
@admin_bp.route('/manage-doctors')
@is_admin_authenticated
def manage_doctors():
    # Fetch doctors (actice, inactive and blacklisted) from the database and display seperately
    active_doctors = doctor.query.filter_by(status='active').all()
    inactive_doctors = doctor.query.filter_by(status='inactive').all()
    blacklisted_doctors = doctor.query.filter_by(status='blacklisted').all()
    return render_template('admin/manage_doctors.html', active_doctors=active_doctors,inactive_doctors=inactive_doctors, blacklisted_doctors=blacklisted_doctors)

# Add doctor route
@admin_bp.route('/add-doctor', methods=['GET', 'POST'])
@is_admin_authenticated
def add_doctor():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        education = request.form.get('education')
        specialization = request.form.get('specialization')
        contact = request.form.get('contact')
        password = request.form.get('password')

        if doctor.query.filter_by(email=email).first():
            flash('Email already exists!', 'danger')
            return redirect(url_for('admin.add_doctor'))

        new_doctor = doctor(name=name, email=email, specialization=specialization, education=education, contact=contact)        
        db.session.add(new_doctor)
        db.session.commit()

        # Also create login credentials for the new doctor
        new_login = login(email=email, password=password, role='doctor')
        db.session.add(new_login)
        db.session.commit()

        flash('Doctor added successfully!', 'success')
        return redirect(url_for('admin.manage_doctors'))

    return render_template('admin/add_doctor.html')


# Delete Doctor Route
@admin_bp.route('/delete-doctor/<int:doctor_id>', methods=['POST'])
@is_admin_authenticated
def delete_doctor(doctor_id):
    doc = doctor.query.get_or_404(doctor_id)

    # Also delete associated login record
    login_record = login.query.filter_by(email=doc.email).first()
    if login_record:
        db.session.delete(login_record)

    db.session.delete(doc)
    db.session.commit()
    flash('Doctor deleted successfully!', 'success')
    return redirect(url_for('admin.manage_doctors'))


# Update Doctor Route
@admin_bp.route('/update-doctor/<int:doctor_id>', methods=['GET', 'POST'])
@is_admin_authenticated
def update_doctor(doctor_id):
    doc = doctor.query.get_or_404(doctor_id)

    if request.method == 'POST':
        doc.name = request.form.get('name')
        doc.email = request.form.get('email')
        doc.education = request.form.get('education')
        doc.specialization = request.form.get('specialization')
        doc.contact = request.form.get('contact')
        doc.experience = request.form.get('experience')
        doc.address = request.form.get('address')
        doc.fees = request.form.get('fees')
        doc.timings = request.form.get('timings')
        doc.days_available = request.form.get('days_available')
        doc.profile_image = request.form.get('profile_image')
        doc.status = request.form.get('status')

        # Also update login email if changed
        login_record = login.query.filter_by(email=doc.email).first()
        if login_record:
            login_record.email = doc.email

        db.session.commit()
        flash('Doctor updated successfully!', 'success')
        return redirect(url_for('admin.manage_doctors'))

    return render_template('admin/update_doctor.html', doctor=doc)


# Search box for doctor Route using AJAX using all the fields
@admin_bp.route('/search-doctors', methods=['GET'])
@is_admin_authenticated
def search_doctors():
    query = request.args.get('query', '')

    results = doctor.query.filter(
        (doctor.name.ilike(f'%{query}%')) |
        (doctor.email.ilike(f'%{query}%')) |
        (doctor.specialization.ilike(f'%{query}%')) |
        (doctor.education.ilike(f'%{query}%')) |
        (doctor.contact.ilike(f'%{query}%')) 
    ).all()

    return render_template('admin/search_results.html', doctors=results)



# Manage Patients Route
@admin_bp.route('/manage-patients')
@is_admin_authenticated
def manage_patients():
    patients = patient.query.filter_by(status='active').all()
    blacklisted_patients = patient.query.filter_by(status='blacklisted').all()

    return render_template('admin/manage_patients.html', patients=patients, blacklisted_patients=blacklisted_patients)

# Delete Patient Route
@admin_bp.route('/delete-patient/<int:patient_id>', methods=['POST'])
@is_admin_authenticated
def delete_patient(patient_id):
    pat = patient.query.get_or_404(patient_id)

    # Also delete associated login record
    login_record = login.query.filter_by(email=pat.email).first()
    if login_record:
        db.session.delete(login_record)

    db.session.delete(pat)
    db.session.commit()
    flash('Patient deleted successfully!', 'success')
    return redirect(url_for('admin.manage_patients'))

# Update Patient Route
@admin_bp.route('/update-patient/<int:patient_id>', methods=['GET', 'POST'])
@is_admin_authenticated
def update_patient(patient_id):
    pat = patient.query.get_or_404(patient_id)

    if request.method == 'POST':
        pat.name = request.form.get('name')
        pat.age = request.form.get('age')
        pat.gender = request.form.get('gender')
        pat.contact = request.form.get('contact')
        pat.email = request.form.get('email')
        pat.address = request.form.get('address')
        pat.medical_history = request.form.get('medical_history')
        pat.blood_group = request.form.get('blood_group')
        pat.family_history = request.form.get('family_history')
        pat.allergies = request.form.get('allergies')
        pat.profile_image = request.form.get('profile_image')
        pat.insurance_details = request.form.get('insurance_details')
        pat.current_medications = request.form.get('current_medications')
        pat.status = request.form.get('status')
        db.session.commit()
        flash('Patient updated successfully!', 'success')
        return redirect(url_for('admin.manage_patients'))
    return render_template('admin/update_patient.html', patient=pat)


# Search box for Patients Route using AJAX using all the fields
@admin_bp.route('/search-patients', methods=['GET'])
@is_admin_authenticated
def search_patients():
    query = request.args.get('query', '')

    results = patient.query.filter(
        (patient.name.ilike(f'%{query}%')) |
        (patient.email.ilike(f'%{query}%')) |
        (patient.contact.ilike(f'%{query}%')) |
        (patient.address.ilike(f'%{query}%')) |
        (patient.medical_history.ilike(f'%{query}%')) |
        (patient.blood_group.ilike(f'%{query}%')) |
        (patient.age.ilike(f'%{query}%')) |
        (patient.current_medications.ilike(f'%{query}%')) |
        (patient.family_history.ilike(f'%{query}%')) |
        (patient.allergies.ilike(f'%{query}%'))
    ).all()

    return render_template('admin/search_results.html', patients=results)

# show appointment details of specific patient seprately for past and upcoming appointments
@admin_bp.route('/patient-appointments/<int:patient_id>')
@is_admin_authenticated
def patient_appointments(patient_id):
    pat = patient.query.get_or_404(patient_id)
    past_appointments = appointment.query.filter(appointment.p_id==patient_id, appointment.date < db.func.current_date()).all()
    upcoming_appointments = appointment.query.filter(appointment.p_id==patient_id, appointment.date >= db.func.current_date()).all()
    return render_template('admin/patient_appointments.html', patient=pat, past_appointments=past_appointments, upcoming_appointments=upcoming_appointments)


# show treatment details of specific patient of specific appointment
@admin_bp.route('/appointment-treatments/<int:appointment_id>')
@is_admin_authenticated
def appointment_treatments(appointment_id):
    appt = appointment.query.get_or_404(appointment_id)
    treatments = treatment.query.filter_by(a_id=appointment_id).all()
    return render_template('admin/appointment_treatments.html', appointment=appt, treatments=treatments)

# show only latest treatment of specific patient
@admin_bp.route('/patient-treatments/<int:patient_id>')
@is_admin_authenticated
def patient_treatments(patient_id):
    pat = patient.query.get_or_404(patient_id)
    treatments = treatment.query.filter_by(p_id=patient_id).order_by(treatment.t_id.desc()).first()
    return render_template('admin/patient_treatments.html', patient=pat, treatments=treatments)


# Show all appointments Route separately for past and upcoming appointments
@admin_bp.route('/manage-appointments')
@is_admin_authenticated
def manage_appointments():
    past_appointments = appointment.query.filter(appointment.date < db.func.current_date()).all()
    upcoming_appointments = appointment.query.filter(appointment.date >= db.func.current_date()).all()
    return render_template('admin/manage_appointments.html', past_appointments=past_appointments, upcoming_appointments=upcoming_appointments) 

# Delete Appointment Route
@admin_bp.route('/delete-appointment/<int:appointment_id>', methods=['POST'])
@is_admin_authenticated
def delete_appointment(appointment_id):
    appt = appointment.query.get_or_404(appointment_id)

    # Also delete associated treatments
    treatments = treatment.query.filter_by(a_id=appt.a_id).all()
    for treat in treatments:
        db.session.delete(treat)

    db.session.delete(appt)
    db.session.commit()
    flash('Appointment and associated treatments deleted successfully!', 'success')
    return redirect(url_for('admin.manage_appointments'))


