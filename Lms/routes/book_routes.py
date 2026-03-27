from flask import *
book_bp = Blueprint('book_bp', __name__)
@book_bp.route('/book-create')
def book_registration():
    return "Book Create Page"
