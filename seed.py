"""
Run this once after creating the database to populate MedNest with demo data:
    python seed.py
"""
from app import create_app
from extensions import db
from models import User, Doctor, DiseaseSpecialty, Medicine, LabTest

app = create_app()

DISEASE_MAP = {
    "fever": "General Physician",
    "flu": "General Physician",
    "cold": "General Physician",
    "cough": "Pulmonologist",
    "asthma": "Pulmonologist",
    "chest pain": "Cardiologist",
    "heart pain": "Cardiologist",
    "high blood pressure": "Cardiologist",
    "skin allergy": "Dermatologist",
    "acne": "Dermatologist",
    "rash": "Dermatologist",
    "toothache": "Dentist",
    "gum pain": "Dentist",
    "eye pain": "Ophthalmologist",
    "blurred vision": "Ophthalmologist",
    "joint pain": "Orthopedic",
    "back pain": "Orthopedic",
    "fracture": "Orthopedic",
    "anxiety": "Psychiatrist",
    "depression": "Psychiatrist",
    "stress": "Psychiatrist",
    "stomach pain": "Gastroenterologist",
    "acidity": "Gastroenterologist",
    "diarrhea": "Gastroenterologist",
    "diabetes": "Endocrinologist",
    "thyroid": "Endocrinologist",
    "pregnancy": "Gynecologist",
    "period pain": "Gynecologist",
    "child fever": "Pediatrician",
    "kidney pain": "Nephrologist",
}

DOCTORS = [
    {"name": "Dr. Ayesha Khan", "email": "ayesha.khan@mednest.com", "specialty": "General Physician",
     "qualification": "MBBS", "exp": 8, "fee": 1000},
    {"name": "Dr. Bilal Ahmed", "email": "bilal.ahmed@mednest.com", "specialty": "Cardiologist",
     "qualification": "MBBS, FCPS (Cardiology)", "exp": 12, "fee": 2500},
    {"name": "Dr. Sana Malik", "email": "sana.malik@mednest.com", "specialty": "Dermatologist",
     "qualification": "MBBS, DDS", "exp": 6, "fee": 1800},
    {"name": "Dr. Usman Tariq", "email": "usman.tariq@mednest.com", "specialty": "Orthopedic",
     "qualification": "MBBS, MS (Ortho)", "exp": 10, "fee": 2000},
    {"name": "Dr. Hira Siddiqui", "email": "hira.siddiqui@mednest.com", "specialty": "Pediatrician",
     "qualification": "MBBS, FCPS (Peds)", "exp": 7, "fee": 1500},
    {"name": "Dr. Omar Farooq", "email": "omar.farooq@mednest.com", "specialty": "Psychiatrist",
     "qualification": "MBBS, FCPS (Psychiatry)", "exp": 9, "fee": 2200},
    {"name": "Dr. Fatima Rauf", "email": "fatima.rauf@mednest.com", "specialty": "Gynecologist",
     "qualification": "MBBS, FCPS (Gynae)", "exp": 11, "fee": 2000},
    {"name": "Dr. Zeeshan Iqbal", "email": "zeeshan.iqbal@mednest.com", "specialty": "Gastroenterologist",
     "qualification": "MBBS, FCPS (Gastro)", "exp": 9, "fee": 2300},
    {"name": "Dr. Nadia Yousaf", "email": "nadia.yousaf@mednest.com", "specialty": "Endocrinologist",
     "qualification": "MBBS, FCPS (Endocrinology)", "exp": 8, "fee": 2100},
    {"name": "Dr. Kamran Sheikh", "email": "kamran.sheikh@mednest.com", "specialty": "Dentist",
     "qualification": "BDS", "exp": 6, "fee": 1200},
    {"name": "Dr. Mahnoor Aslam", "email": "mahnoor.aslam@mednest.com", "specialty": "Ophthalmologist",
     "qualification": "MBBS, FCPS (Ophthalmology)", "exp": 7, "fee": 1700},
    {"name": "Dr. Adeel Rashid", "email": "adeel.rashid@mednest.com", "specialty": "Pulmonologist",
     "qualification": "MBBS, FCPS (Pulmonology)", "exp": 10, "fee": 2000},
    {"name": "Dr. Sara Naveed", "email": "sara.naveed@mednest.com", "specialty": "Nephrologist",
     "qualification": "MBBS, FCPS (Nephrology)", "exp": 9, "fee": 2400},
]

MEDICINES = [
    {"name": "Panadol 500mg", "category": "Analgesic", "stock": 200, "price": 5},
    {"name": "Augmentin 625mg", "category": "Antibiotic", "stock": 120, "price": 45},
    {"name": "Brufen 400mg", "category": "Anti-inflammatory", "stock": 150, "price": 12},
    {"name": "Cetirizine 10mg", "category": "Antihistamine", "stock": 100, "price": 8},
    {"name": "Omeprazole 20mg", "category": "Antacid", "stock": 90, "price": 15},
    {"name": "Amlodipine 5mg", "category": "Antihypertensive", "stock": 80, "price": 20},
]

LAB_TESTS = [
    {"name": "Complete Blood Count (CBC)", "price": 800, "description": "General blood health screening"},
    {"name": "Blood Sugar (Fasting)", "price": 400, "description": "Diabetes screening"},
    {"name": "Lipid Profile", "price": 1500, "description": "Cholesterol & heart risk profile"},
    {"name": "Liver Function Test", "price": 1800, "description": "Liver health screening"},
    {"name": "X-Ray", "price": 1200, "description": "Imaging for bones & chest"},
    {"name": "ECG", "price": 1000, "description": "Heart electrical activity"},
]


def seed():
    with app.app_context():
        db.create_all()

        # Admin account
        if not User.query.filter_by(email="admin@mednest.com").first():
            admin = User(name="MedNest Admin", email="admin@mednest.com", role="admin")
            admin.set_password("admin123")
            db.session.add(admin)

        # Sample staff accounts
        staff_defaults = [
            ("Reception Desk", "reception@mednest.com", "receptionist"),
            ("Pharmacy Desk", "pharmacy@mednest.com", "pharmacist"),
            ("Lab Desk", "lab@mednest.com", "lab_tech"),
        ]
        for name, email, role in staff_defaults:
            if not User.query.filter_by(email=email).first():
                u = User(name=name, email=email, role=role)
                u.set_password("staff123")
                db.session.add(u)

        db.session.commit()

        # Doctors
        for doc in DOCTORS:
            if not User.query.filter_by(email=doc["email"]).first():
                u = User(name=doc["name"], email=doc["email"], role="doctor")
                u.set_password("doctor123")
                db.session.add(u)
                db.session.flush()
                profile = Doctor(
                    user_id=u.id,
                    specialty=doc["specialty"],
                    qualification=doc["qualification"],
                    experience_years=doc["exp"],
                    consultation_fee=doc["fee"],
                    bio=f"Experienced {doc['specialty']} with {doc['exp']} years of practice.",
                )
                db.session.add(profile)

        # Disease -> specialty map
        for disease, specialty in DISEASE_MAP.items():
            if not DiseaseSpecialty.query.filter_by(disease=disease).first():
                db.session.add(DiseaseSpecialty(disease=disease, specialty=specialty))

        # Medicines
        for m in MEDICINES:
            if not Medicine.query.filter_by(name=m["name"]).first():
                db.session.add(Medicine(name=m["name"], category=m["category"],
                                         stock_qty=m["stock"], unit_price=m["price"], reorder_level=20))

        # Lab tests
        for t in LAB_TESTS:
            if not LabTest.query.filter_by(name=t["name"]).first():
                db.session.add(LabTest(name=t["name"], price=t["price"], description=t["description"]))

        db.session.commit()
        print("MedNest seeded successfully!")
        print("Login as admin: admin@mednest.com / admin123")
        print("Login as receptionist: reception@mednest.com / staff123")
        print("Login as pharmacist: pharmacy@mednest.com / staff123")
        print("Login as lab tech: lab@mednest.com / staff123")
        print("Login as any doctor: <email above> / doctor123")


if __name__ == "__main__":
    seed()
