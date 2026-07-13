from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db, login_manager

# ---------------------------------------------------------------------------
# Roles used across the system
# ---------------------------------------------------------------------------
ROLES = ["patient", "doctor", "receptionist", "pharmacist", "lab_tech", "admin"]


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(30))
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # role-specific profiles (one will be populated depending on role)
    doctor_profile = db.relationship("Doctor", backref="user", uselist=False, cascade="all, delete-orphan")
    patient_profile = db.relationship("Patient", backref="user", uselist=False, cascade="all, delete-orphan")

    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password_hash, raw)

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(150))
    experience_years = db.Column(db.Integer, default=0)
    consultation_fee = db.Column(db.Integer, default=0)
    available_days = db.Column(db.String(150), default="Mon-Sat")
    bio = db.Column(db.Text)

    appointments = db.relationship("Appointment", backref="doctor", lazy=True)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    blood_group = db.Column(db.String(10))
    address = db.Column(db.String(250))

    appointments = db.relationship("Appointment", backref="patient", lazy=True)


class DiseaseSpecialty(db.Model):
    """Maps a disease / symptom keyword to the specialty that treats it."""
    id = db.Column(db.Integer, primary_key=True)
    disease = db.Column(db.String(120), unique=True, nullable=False)
    specialty = db.Column(db.String(100), nullable=False)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    disease = db.Column(db.String(150))
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="pending")
    # pending -> confirmed -> checked_in -> completed / cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    prescription = db.relationship("Prescription", backref="appointment", uselist=False, cascade="all, delete-orphan")
    lab_orders = db.relationship("LabOrder", backref="appointment", cascade="all, delete-orphan")


class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointment.id"), nullable=False)
    diagnosis = db.Column(db.Text)
    advice = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship("PrescriptionItem", backref="prescription", cascade="all, delete-orphan")


class PrescriptionItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey("prescription.id"), nullable=False)
    medicine_name = db.Column(db.String(150), nullable=False)
    dosage = db.Column(db.String(80))
    frequency = db.Column(db.String(80))
    duration = db.Column(db.String(80))
    dispensed = db.Column(db.Boolean, default=False)


class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    category = db.Column(db.String(80))
    stock_qty = db.Column(db.Integer, default=0)
    unit_price = db.Column(db.Float, default=0.0)
    expiry_date = db.Column(db.Date)
    reorder_level = db.Column(db.Integer, default=20)


class LabTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    price = db.Column(db.Integer, default=0)
    description = db.Column(db.String(250))

    orders = db.relationship("LabOrder", backref="test", lazy=True)


class LabOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointment.id"), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey("lab_test.id"), nullable=False)
    status = db.Column(db.String(20), default="ordered")
    # ordered -> sample_collected -> completed
    ordered_at = db.Column(db.DateTime, default=datetime.utcnow)

    result = db.relationship("LabResult", backref="order", uselist=False, cascade="all, delete-orphan")


class LabResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lab_order_id = db.Column(db.Integer, db.ForeignKey("lab_order.id"), nullable=False)
    result_text = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
