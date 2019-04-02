from flask import Blueprint

bp = Blueprint('faculties', __name__)

from app.faculties import routes
