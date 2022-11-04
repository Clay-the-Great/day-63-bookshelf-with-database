import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()
# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, "
#                "author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()

# Use flask_sqlalchemy
app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


# db.create_all()
# harry = Books(
#     id=1,
#     title="Harry Potter",
#     author="J. K. Rowling",
#     rating=9.3
# )
# db.session.add(harry)
# db.session.commit()

all_books = Books.query.all()
print(all_books[0].title)
# book = Books.query.filter_by(title="Harry Potter").first()
# print(book.title)
# book.title = "Harry Potter and the Chamber of Secrets"
# db.session.commit()

# book_id = 1
# book_to_update = Books.query.get(book_id)
# book_to_update.title = "Harry Potter and the Goblet of Fire"
# db.session.commit()

# book_to_delete = Books.query.get(book_id)
# db.session.delete(book_to_delete)
# db.session.commit()