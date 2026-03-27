from flask import *
from models import *
from flask import flash
from flask_bcrypt import Bcrypt
from db import db
bcrypt = Bcrypt()
student_bp=Blueprint("student",__name__)

# student register
@student_bp.route("/student-register",methods=["POST","GET"])
def student_register():
    if request.method=="POST":
        form_stu_name=request.form.get("stu_name")
        form_stu_age=request.form.get("stu_age")
        form_stu_email=request.form.get("stu_email")
        form_stu_phone=request.form.get("stu_phone")
        form_stu_address=request.form.get("stu_address")
        form_stu_password=request.form.get("stu_password")
        hashed_password=bcrypt.generate_password_hash(form_stu_password).decode('utf-8')

        try:
            stu_data=Student(
            stu_name=form_stu_name,
            stu_age=form_stu_age,
            stu_email=form_stu_email,
            stu_phone=form_stu_phone,
            stu_address=form_stu_address,
            stu_password=hashed_password,
            role="student"
            )
        
            db.session.add(stu_data)
            db.session.commit()
            return redirect(url_for("student.all_students_data"))
        
        except Exception as e:
            return str(e)  
    
    else:
        return render_template("students/register-student.html")



@student_bp.route("/all-student")
def all_students_data():
    get_students=Student.query.all() # select * from student
    return render_template("students/all_students.html",students=get_students)

@student_bp.route("/student-details/<int:id>")
def students_details(id):
   get_stu=Student.query.get(id)
   return render_template("students/student-details.html",student=get_stu)

@student_bp.route("/student-delete/<int:id>")
def students_delete(id):
   student=Student.query.get_or_404(id)
   db.session.delete(student)
   db.session.commit()
   return redirect(url_for("student.all_students_data"))


@student_bp.route("/student-update/<int:id>",methods=["GET","POST"])
def students_update(id):
   student=Student.query.get_or_404(id)
   if request.method=="POST":
        student.stu_name=request.form.get("stu_name")
        student.stu_age=request.form.get("stu_age")
        student.stu_email=request.form.get("stu_email")
        student.stu_phone=request.form.get("stu_phone")
        student.stu_address=request.form.get("stu_address")
        db.session.commit()
        flash("Student details updated successfully!")
        return redirect(url_for("student.all_students_data"))
   return render_template("students/update-student.html", student=student)    