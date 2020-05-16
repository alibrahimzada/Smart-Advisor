import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.auth import login_required
from flaskr.user import Student
from flaskr.testimonials import fetch_testifiers, save_testimony
from flaskr.scrapers.sap_scraper import fetch_transcript

bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/')
@login_required
def profile():
    current_user = g.user
    block, radio, label = fetch_testifiers()
    student_number, semester_of_student, advisor, standing, gpa, completed_credits, completed_ects, department = Student.get_details(current_user[0])
    graduation_progress = 100
    if department != None:
        graduation_progress = Student.graduation_progress(department, current_user[0])
    return render_template('profile/profile.html', name=current_user[2], email=current_user[3], profile_pic=current_user[4], testifiers=block, radio_buttons=radio, labels=label,
                           student_number=student_number, semester_of_student=semester_of_student, advisor=advisor, standing=standing, gpa=gpa, completed_credits=completed_credits,
                           completed_ects=completed_ects, department=department, graduation_progress=graduation_progress)

@bp.route('/fetch_sap', methods=['POST', 'GET'])
@login_required
def fetch_sap():
    current_user = g.user
    if request.method == 'GET':
        return render_template('profile/fetch_sap.html', name=current_user[2], profile_pic=current_user[4])
    else:
        email = request.form['email']
        password = request.form['password']
        fetch_transcript(email, password, current_user[0])
        return redirect(url_for('profile.profile'))

@bp.route('/predict', methods=['POST', 'GET'])
@login_required
def predict():
    current_user = g.user
    subjects = []
    with open(os.getcwd() + '/Smart-Advisor/flaskr/data/subject_names.txt') as subject_names:
        for subject in subject_names:
            subjects.append(subject.strip())
            
    if request.method == 'GET':
        return render_template('profile/predict.html', name=current_user[2], profile_pic=current_user[4], subjects=subjects)
    else:
        a = request.form.getlist('options[]')
        print(a)
        return render_template('profile/predict.html', name=current_user[2], profile_pic=current_user[4])

@bp.route('/rate_instructor')
@login_required
def rate_instructor():
    current_user = g.user
    return render_template('profile/rate_instructor.html', name=current_user[2], profile_pic=current_user[4])


@bp.route('/rate_course')
@login_required
def rate_course():
    current_user = g.user
    return render_template('profile/rate_course.html', name=current_user[2], profile_pic=current_user[4])

@bp.route('/analyze_instructor')
@login_required
def analyze_instructor():
    current_user = g.user
    return render_template('profile/analyze_instructor.html', name=current_user[2], profile_pic=current_user[4])

@bp.route('/analyze_course')
@login_required
def analyze_course():
    current_user = g.user
    return render_template('profile/analyze_course.html', name=current_user[2], profile_pic=current_user[4])

@bp.route('/testify', methods=['POST', 'GET'])
@login_required
def testify():
    current_user = g.user
    if request.method == 'GET':
        return render_template('profile/testimonial.html', name=current_user[2], profile_pic=current_user[4])
    else:
        headline = request.form['headline']
        testimony = request.form['testimony']
        save_testimony(testimony, headline, current_user[0])
        return redirect(url_for('profile.profile'))


@bp.route('/handle_rating', methods=['POST', 'GET'])
@login_required
def handle_rating():
    return redirect(url_for('profile.profile'))
