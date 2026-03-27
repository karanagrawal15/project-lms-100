from flask import *
from models import *
from flask import flash
from flask_bcrypt import Bcrypt
from db import db
bcrypt = Bcrypt()
author_bp=Blueprint("author",__name__)

# author register
@author_bp.route("/author-register",methods=["POST","GET"])
def author_register():
    if request.method=="POST":
        form_author_name=request.form.get("author_name")
        form_author_age=request.form.get("author_age")
        form_author_email=request.form.get("author_email")
        form_author_phone=request.form.get("author_phone")
        form_author_address=request.form.get("author_address")
        form_author_password=request.form.get("author_password")
        hashed_password=bcrypt.generate_password_hash(form_author_password).decode('utf-8')

        try:
            author_data=Author(
            author_name=form_author_name,
            author_age=form_author_age,
            author_email=form_author_email,
            author_phone=form_author_phone,
            author_address=form_author_address,
            author_password=hashed_password,
            role="author"
            )
        
            db.session.add(author_data)
            db.session.commit()
            return redirect(url_for("author.all_authors_data"))
        
        except Exception as e:
            return str(e)  
    
    else:
        return render_template("author/register-author.html")



@author_bp.route("/all-author")
def all_authors_data():
    get_authors=Author.query.all() # select * from author
    return render_template("author/all_authors.html",authors=get_authors)

@author_bp.route("/author-details/<int:id>")
def authors_details(id):
   get_author=Author.query.get(id)
   return render_template("author/author-details.html",author=get_author)

@author_bp.route("/author-delete/<int:id>")
def authors_delete(id):
   author=Author.query.get_or_404(id)
   db.session.delete(author)
   db.session.commit()
   return redirect(url_for("author.all_authors_data"))


@author_bp.route("/author-update/<int:id>",methods=["GET","POST"])
def authors_update(id):
   author=Author.query.get_or_404(id)
   if request.method=="POST":
        author.author_name=request.form.get("author_name")
        author.author_age=request.form.get("author_age")
        author.author_email=request.form.get("author_email")
        author.author_phone=request.form.get("author_phone")
        author.author_address=request.form.get("author_address")
        db.session.commit()
        flash("Author details updated successfully!")
        return redirect(url_for("author.all_authors_data"))
   return render_template("author/update-author.html", author=author)    