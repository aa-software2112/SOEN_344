from flask import Flask

app = Flask(__name__)

# Routes
from app.views import index_route
