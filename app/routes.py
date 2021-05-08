from app import db
from app.models.book import Book
from flask import request
from flask import request, Blueprint, make_response
from flask import jsonify

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("/<book_id>", methods=["GET", "PUT","DELETE"], strict_slashes=False)
# this function get data from one book and also updates data.
def handle_book(book_id):
    # Try to find the book with the given id

    book = Book.query.get(book_id)

    if book is None:
        return make_response("", 404)

    if request.method == "GET":
        
        return {
            "id": book.id,
            "title": book.title,
            "description": book.description
        }

    elif request.method == "PUT":
        form_data = request.get_json()

        book.title = form_data["title"]
        book.description = form_data["description"]

        db.session.commit()

        return make_response(f"Book #{book.id} successfully updated")

    elif request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
        return make_response(f"Book #{book.id} successfully deleted")
    
    
    return {
        "message": f"Book with id {book_id} was not found",
        "success": False,
    }, 404
    

@books_bp.route("", methods=["POST", "GET"], strict_slashes=False)
def books():
    if request.method == "GET":
        book_title = request.args.get("title")
        if book_title != None:
            books = Book.query.filter_by(title=book_title)
        else:
            books = Book.query.all()
        books_response = []
        for book in books:
            books_response.append({
                "id": book.id,
                "title": book.title,
                "description": book.description
            })
        return jsonify(books_response)
    

    else:
        request_body = request.get_json()
        new_book = Book(title = request_body["title"],
                            description = request_body["description"])

        db.session.add(new_book)
        db.session.commit()

        return make_response(f"Book {new_book.title} successfully created", 201)



# hello_world_bp = Blueprint("hello_world", __name__)


# @hello_world_bp.route("/hello-world", methods=["GET"])
# def say_hello_world():
#     my_response_body = "Hello, World!"
#     return my_response_body


# @hello_world_bp.route("/hello/JSON", methods=["GET"])
# def hello_world_json():
#     return {
#         "name": "Glenda Chicas",
#         "message": "Hola",
#         "hobbies": ["hiking", "speding time with family", "handing out with friends"]
#     }

# @hello_world_bp.route("/broken-endpoint-with-broken-server-code")
# def broken_endpoint():
#     response_body = {
#         "name": "Ada Lovelace",
#         "message": "Hello!",
#         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
#     }
#     new_hobby = "Surfing"
#     response_body["hobbies"].append(new_hobby)
#     return response_body


