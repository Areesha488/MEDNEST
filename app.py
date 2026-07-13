from flask import Flask, render_template, redirect, url_for
from flask_login import current_user

from config import Config
from extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from blueprints.auth import auth_bp
    from blueprints.patient import patient_bp
    from blueprints.doctor import doctor_bp
    from blueprints.reception import reception_bp
    from blueprints.pharmacy import pharmacy_bp
    from blueprints.lab import lab_bp
    from blueprints.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(reception_bp)
    app.register_blueprint(pharmacy_bp)
    app.register_blueprint(lab_bp)
    app.register_blueprint(admin_bp)

    @app.route("/")
    def home():
        if current_user.is_authenticated:
            role_home = {
                "patient": "patient.dashboard",
                "doctor": "doctor.dashboard",
                "receptionist": "reception.dashboard",
                "pharmacist": "pharmacy.dashboard",
                "lab_tech": "lab.dashboard",
                "admin": "admin.dashboard",
            }
            return redirect(url_for(role_home.get(current_user.role, "auth.login")))
        return render_template("index.html")

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
