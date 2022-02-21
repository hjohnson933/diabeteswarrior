from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from diabeteswarrior import db
from diabeteswarrior.models import Scan
from diabeteswarrior.scans.forms import ScanForm

scans = Blueprint('scans', __name__)
