import os

from flask import Flask, request, redirect, url_for
from flask import render_template
from sqlalchemy import desc

from database import db, Book, Genre, Author

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    # creating and adding genres
    comedy = Genre(name='Комедия')
    db.session.add(comedy)
    story = Genre(name='Повесть')
    db.session.add(story)

    # creating and adding authors
    fonvizin = Author(name='Д.И.Фонвизин')
    db.session.add(fonvizin)
    griboedov = Author(name='А.С.Грибоедов')
    db.session.add(griboedov)
    pushkin = Author(name='А.С.Пушкин')
    db.session.add(pushkin)

    # creating and adding books
    nedorosl = Book(name='Недоросль', genre=comedy, author=fonvizin)
    db.session.add(nedorosl)
    woe_from_wit = Book(name='Горе от ума', genre=comedy, author=griboedov)
    db.session.add(woe_from_wit)
    capitans_daughter = Book(name='Капитанская дочка', genre=story, author=pushkin)
    db.session.add(capitans_daughter)

    db.session.commit()


@app.route("/", methods=['GET', 'POST'])
def all_books():
    if request.method == 'POST':
        book_id = request.form.get('is_read')
        if book_id:
            book = Book.query.get(book_id)
            book.is_read = True
            db.session.commit()

    books = Book.query.order_by(desc(Book.added)).limit(15).all()
    return render_template("books.html", books=books)


@app.route("/genre/<int:genre_id>")
def books_by_genres(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    return render_template(
        "books_by_genres.html",
        genre_name=genre.name,
        books=genre.books,
    )


@app.route("/author/<int:author_id>")
def books_by_author(author_id):
    author = Author.query.get_or_404(author_id)
    return render_template(
        "books_by_author.html",
        author_name=author.name,
        books=author.books
    )

# section to add book to database
@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        book_name, book_author, book_genre = request.form.get('name'), request.form.get('author'), request.form.get(
            'genre')
        book = Book(name=book_name, genre=book_genre, author=book_author)
        db.session.add(book)
        db.session.commit()
        redirect(url_for("/"))

    return render_template("add_book.html")


if __name__ == '__main__':
    app.run()
