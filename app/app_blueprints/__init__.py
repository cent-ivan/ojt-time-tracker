#Centralized blueprint imports
from .auth import auth_bp
from .dashboard.student_dashboard import stud_dashboard_bp
from .public import public_bp

all_blueprints = [
    (public_bp, '/'),
    (auth_bp, '/auth'),
    (stud_dashboard_bp, '/student-dashboard')
]