from flask import *
from flask_bcrypt import Bcrypt
from routes.students_routes import *
from routes.authors_routes import *
from flask_migrate import Migrate
from models import *
from sqlalchemy import text

from db import *
from config import Config

app = Flask(__name__)

app.secret_key = "this-is-mylibrary-app"

app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt()
bcrypt.init_app(app)


# Database health check
@app.route("/db-health")
def db_health():
    try:
        db.session.execute(text("SELECT 1"))
        return {"status": "Ok", "database": "Connected"}
    except Exception as e:
        return {"status": str(e)}


# Home Page
@app.route("/")
def home():
    return render_template("home.html")


# Logout
@app.route("/logout")
def user_logout():
    session.pop("user_id", None)
    return redirect(url_for("home"))


# =============================
# STUDENT LOGIN
# =============================
@app.route("/student-login", methods=["POST", "GET"])
def student_login():

    if request.method == "POST":

        email = request.form.get("user_email")
        password = request.form.get("user_password")

        user = Student.query.filter_by(stu_email=email).first()

        if user and bcrypt.check_password_hash(user.stu_password, password):

            session["user_id"] = user.id
            session["role"] = "student"

            flash("Student Login successful", "success")
            return redirect(url_for("student.all_students_data"))

        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")


# =============================
# AUTHOR LOGIN
# =============================
@app.route("/author-login", methods=["POST", "GET"])
def author_login():

    if request.method == "POST":

        email = request.form.get("author_email")
        password = request.form.get("author_password")

        author = Author.query.filter_by(author_email=email).first()

        if author and bcrypt.check_password_hash(author.author_password, password):

            session["user_id"] = author.id
            session["role"] = "author"

            flash("Author Login successful", "success")
            return redirect(url_for("author.all_authors_data"))

        else:
            flash("Invalid email or password", "danger")

    return render_template("author-login.html")


# =============================
# BLUEPRINTS
# =============================

# Student Routes
app.register_blueprint(student_bp, url_prefix="/student")

# Author Routes
app.register_blueprint(author_bp, url_prefix="/author")


#============================
# LOGIN 
#============================

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == "POST":
        email = request.form['user_email']
        password = request.form['user_password']

        print(email)
        print(password)

    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)