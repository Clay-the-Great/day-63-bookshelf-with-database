from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-collection.db"
db = SQLAlchemy(app)
# all_books_array = []


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
# db.create_all()


class DeletionForm(FlaskForm):
    delete = SubmitField(label="Delete")
    cancel = SubmitField(label="Cancel")


@app.route('/')
def home():
    all_books = Books.query.all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        # new_book = {
        #     "title": request.form["title"],
        #     "author": request.form["author"],
        #     "rating": request.form["rating"],
        # }
        # all_books_array.append(new_book)
        new_book_db = Books(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_book_db)
        db.session.commit()

        return redirect(url_for("home"))
    return render_template("add.html")


@app.route("/edit/<book_id>", methods=["POST", "GET"])
def edit_rating(book_id):
    book_to_update = Books.query.filter_by(id=book_id).first()
    if request.method == "POST":
        new_rating = request.form["new_rating"]
        book_to_update.rating = float(new_rating)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit_rating.html", book=book_to_update)


@app.route("/delete/<book_id>", methods=["POST", "GET"])
def delete_book(book_id):
    book_to_delete = Books.query.get(book_id)
    deletion_form = DeletionForm(meta={'csrf': False})
    if deletion_form.validate_on_submit():
        if deletion_form.cancel.data:
            return redirect(url_for("home"))
        elif deletion_form.delete.data:
            db.session.delete(book_to_delete)
            db.session.commit()
            return redirect(url_for("home"))
    return render_template("deletion.html", form=deletion_form, book_to_delete=book_to_delete)


if __name__ == "__main__":
    app.run(debug=True)
