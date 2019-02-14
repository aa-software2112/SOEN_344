from flask import Blueprint
controllers = Blueprint('controllers', __name__)

from .availability_controller import *
from .booking_controller import *
from .patient_controller import *
