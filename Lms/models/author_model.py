from db import *

class Author(db.Model):
    __tablename__="authors"
    id=db.Column(db.Integer,primary_key=True)
    author_name=db.Column(db.String(100),nullable=False)
    author_age=db.Column(db.DateTime,nullable=False)
    author_email=db.Column(db.String(100),unique=True)
    author_phone=db.Column(db.String(11),nullable=False,unique=True)
    author_password=db.Column(db.String(200),nullable=False)
    author_address=db.Column(db.String(200),nullable=False)
    role=db.Column(db.String(20),nullable=False)