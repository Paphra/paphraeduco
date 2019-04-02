from flask import Blueprint

bp = Blueprint()

from app.groups import forms, routes
