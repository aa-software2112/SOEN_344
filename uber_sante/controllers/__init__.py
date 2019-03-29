from flask import Blueprint

controllers = Blueprint('controllers', __name__)

from .availability_controller import *
from .booking_controller import *
from .patient_controller import *
from .admin_controller import *
from .doctor_controller import *
from .nurse_controller import *
from .login_controller import *
from .clinic_controller import *

@controllers.route('/')
def index():
    return 'Welcome to Uber Sante!'
