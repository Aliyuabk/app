from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from werkzeug.utils import secure_filename
import os

from config import Config
from models import db, admin, courses

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.secret_key = "super-secret-key"

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Create tables
with app.app_context():
    db.create_all()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash("Please log in first", "warning")
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function
# Home page
@app.route('/')
def index():
    all_courses = courses.query.all()
    return render_template('index.html', title="Home Page", courses=all_courses)

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    return render_template('admin/admin.html', title="Admin Dashboard")


@app.route('/addcourses', methods=['GET', 'POST'])
@login_required
def addcourses():
    if request.method == 'POST':
        cname = request.form.get('cname')
        price = request.form.get('price')
        grant = request.form.get('grant')
        month = request.form.get('month')
        description = request.form.get('description')

        new_course = courses(
            cname=cname,
            price=price,
            grant=grant,
            month=month,
            description=description
        )

        db.session.add(new_course)
        db.session.commit()

        flash("Course added successfully", "success")
        return redirect(url_for('addcourses'))

    return render_template('admin/addcourses.html', title="Add Courses")


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = admin.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:
            session['admin_logged_in'] = True
            session['admin_username'] = user.username
            flash("Login successful", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for('admin_login'))

    return render_template('admin/admin_login.html', title="Admin Login")


# with app.app_context():
#     new_admin = admin(username="08034897634", password="1234")
#     db.session.add(new_admin)
#     db.session.commit()


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out successfully", "info")
    return redirect(url_for('admin_login'))

if __name__ == "__main__":
    app.run(debug=True)
