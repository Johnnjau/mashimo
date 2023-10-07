from unicodedata import category
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Recipe, User
from .import db
import json
from import csrf

views = Blueprint('views', __name__)

@views.route('/about')
def about():
    """Returns about page"""
    return render_template('about.html')

@views.route('/')
def home():
    """Returns home page"""