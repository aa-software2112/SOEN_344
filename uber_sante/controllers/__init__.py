from flask import Blueprint

controllers = Blueprint('controllers', __name__)


@controllers.route('/')
def index():
    return 'Welcome to Uber Sante!'
