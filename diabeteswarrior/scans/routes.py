from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from diabeteswarrior import db
from diabeteswarrior.models import Scan
from diabeteswarrior.scans.forms import ScanForm

scans = Blueprint('scans', __name__)

@scans.route("/scan")
def home():
    return render_template('scans/home.html')

@scans.route('/scan/new', methods=['GET', 'POST'])
@login_required
def new_scan():
    title = 'New Scan Record'
    form = ScanForm()
    if form.validate_on_submit():
        # pylint: disable=redefined-outer-name
        scan = Scan(author=current_user, message=form.message.data, glucose=form.glucose.data, trend=form.trend.data, notes=form.notes.data, bolus=form.bolus.data, bolus_u=form.bolus_u.data, basal=form.basal.data, basal_u=form.basal_u.data, food=form.food.data, food_u=form.food_u.data, medication=form.medication.data, exercise=form.exercise.data, lower_limit=form.lower_limit.data, upper_limit=form.upper_limit.data)
        db.session.add(scan)
        db.session.commit()
        flash('Your scan record has been created.', 'success')
        return redirect(url_for('scans.home'))
    return render_template('scans/create_scan.html', title=title, form=form, legend=title)

@scans.route('/scan/<int:scan_id>')
def scan(scan_id):
    # pylint: disable=redefined-outer-name
    scan = Scan.query.get_or_404(scan_id)
    return render_template('scans/scan.html', title=scan.title, scan=scan)

@scans.route('/scan/<int:scan_id>/update', methods=['GET', 'POST'])
@login_required
def update_scan(scan_id):
    title='Update Scan'
    # pylint: disable=redefined-outer-name
    scan = Scan.query.get_or_404(scan_id)
    if scan.author != current_user:
        abort(403)
    form = ScanForm()
    if form.validate_on_submit():
        scan.title = form.title.data
        scan.message = form.message.data
        scan.glucose = form.glucose.data
        scan.trend = form.trend.data
        scan.notes = form.notes.data
        scan.bolus = form.bolus.data
        scan.bolus_u = form.bolus_u.data
        scan.basal = form.basal.data
        scan.basal_u = form.basal_u.data
        scan.food = form.food.data
        scan.food_u = form.food_u.data
        scan.medication = form.medication.data
        scan.exercise = form.exercise.data
        scan.lower_limit = form.lower_limit.data
        scan.upper_limit = form.upper_limit.data
        db.session.commit()
        flash('Your scan record has been updated!', 'success')
    elif request.method == 'GET':
        form.title.data = scan.title
        form.message.data = scan.message
        form.glucose.data = scan.glucose
        form.trend.data = scan.trend
        form.notes.data = scan.notes
        form.bolus.data = scan.bolus
        form.bolus_u.data = scan.bolus_u
        form.basal.data = scan.basal
        form.basal_u.data = scan.basal_u
        form.food.data = scan.food
        form.food_u.data = scan.food_u
        form.medication.data = scan.medication
        form.exercise.data = scan.exercise
        form.lower_limit.data = scan.lower_limit
        scan.upper_limit = form.upper_limit.data
    return render_template('scans/create_scan.html', title=title, form=form, legend=title)

@scans.route('/scan/<int:scan_id>/delete', methods=['POST'])
@login_required
def delete_scan(scan_id):
    # pylint: disable=redefined-outer-name
    scan = Scan.query.get_or_404(scan_id)
    if Scan.author != current_user:
        abort(403)
    db.session.delete(scan)
    db.session.commit()
    flash('Yourscan record has been deleted!', 'success')
    return redirect(url_for('scans.home'))
