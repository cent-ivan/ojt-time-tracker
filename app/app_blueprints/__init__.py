#Centralized blueprint imports
from .auth import auth_bp
from .home import home_bp
from .core import core_bp

all_blueprints = [
    (core_bp, '/'),
    (auth_bp, '/auth'),
    (home_bp, '/dashboard')
]