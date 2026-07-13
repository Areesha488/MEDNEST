# MedNest — Online Medical Screening & Hospital Management System

One dashboard that connects every part of a clinic's day-to-day workflow: patients, doctors,
reception, pharmacy and the diagnostic lab.

## Roles & what each one can do

| Role | Capabilities |
|---|---|
| **Patient** | Register/login, search for a doctor by disease or symptom, request an appointment, view prescriptions, view lab reports |
| **Doctor** | See today's checked-in patient queue, open a consultation, write diagnosis + prescription, order lab tests |
| **Receptionist** | Confirm pending appointment requests, check patients in on arrival, view full appointment history |
| **Pharmacist** | See pending prescriptions to dispense, manage medicine stock/inventory, get low-stock alerts |
| **Lab Technician** | See ordered tests, mark sample collected, upload results |
| **Admin** | View system-wide stats, add lab tests, manage the disease → specialty mapping used by patient search |

## How the disease search works

Patients type a symptom or disease (e.g. "chest pain", "skin allergy"). MedNest looks it up in
a `DiseaseSpecialty` table that maps that keyword to a specialty (e.g. Cardiologist,
Dermatologist), then shows every doctor registered under that specialty. Admins can add new
mappings from the Admin Panel as the clinic adds more conditions/specialties.

## Tech stack

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login
- **Database:** SQLite (swap the URI in `config.py` for Postgres/MySQL in production)
- **Frontend:** Server-rendered Jinja2 templates + Bootstrap 5, custom navy/gold theme

## Project structure

```
mednest/
├── app.py                 # app factory + role-based home redirect
├── config.py
├── extensions.py          # db, login_manager
├── models.py              # all database tables
├── seed.py                # demo data: doctors, medicines, lab tests, disease map
├── requirements.txt
├── blueprints/
│   ├── auth.py            # register/login/logout
│   ├── patient.py         # find doctor, book appointment, prescriptions, lab reports
│   ├── doctor.py          # queue + consultation/prescription writing
│   ├── reception.py       # confirm/check-in/cancel appointments
│   ├── pharmacy.py        # inventory + dispensing
│   ├── lab.py             # test orders + result upload
│   └── admin.py           # stats, lab test & disease-map management
├── templates/              # one folder per role, plus shared base.html
└── static/css/style.css    # navy/gold theme
```

## Setup (run locally)

```bash
cd mednest
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python seed.py                  # creates the DB and loads demo data
python app.py                   # starts the dev server on http://127.0.0.1:5000
```

## Demo logins (created by `seed.py`)

| Role | Email | Password |
|---|---|---|
| Admin | admin@mednest.com | admin123 |
| Receptionist | reception@mednest.com | staff123 |
| Pharmacist | pharmacy@mednest.com | staff123 |
| Lab Tech | lab@mednest.com | staff123 |
| Doctor (any of 6 seeded) | e.g. ayesha.khan@mednest.com | doctor123 |

Register a new **Patient** account yourself from the "Get Started" button — that's the one role
meant for open self-signup.

## A typical patient journey through the system

1. Patient registers, then searches "chest pain" under **Find a Doctor** → matched to Cardiologist.
2. Patient requests an appointment with a listed doctor.
3. **Reception** confirms the request, and checks the patient in on the day of the visit.
4. **Doctor** sees the patient in today's queue, opens the consultation, records diagnosis, writes
   medicines, and optionally orders a lab test.
5. **Pharmacy** sees the new prescription items and dispenses them against live stock.
6. **Lab** collects the sample, then uploads the result once ready.
7. Patient can see the finished prescription and lab result on their own dashboard.

## Before using this in a real clinic

This is a complete, working prototype built for a portfolio/academic submission — a few things
to harden before real patient data touches it:
- Restrict staff role registration to admin-only invites (currently open for demo convenience).
- Move off SQLite to Postgres/MySQL, and enable HTTPS.
- Add audit logging and stricter access control per Pakistan's/your institution's data-protection
  expectations for medical records.
- Store lab result files (not just text) with proper access-controlled storage.
- Rotate the `SECRET_KEY` in `config.py` and load it from an environment variable.
